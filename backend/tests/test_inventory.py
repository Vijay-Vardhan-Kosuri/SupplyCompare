from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from apps.accounts.models import User, RetailerProfile
from apps.catalog.models import ProductCategory, Product
from apps.suppliers.models import Supplier
from apps.purchasing.models import PurchaseOrder, PurchaseOrderItem
from apps.inventory.models import StockItem, StockMovement
from apps.accounts.authentication import generate_tokens_for_user

class InventoryAndReceiptTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.retailer = User.objects.create_user(
            email='inv_retailer@supplycompare.local',
            password='TestPassword123',
            role='retailer'
        )
        RetailerProfile.objects.create(user=self.retailer, shop_name='Inventory Test Store')
        token = generate_tokens_for_user(self.retailer)['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.supplier = Supplier.objects.create(
            name='Test Agro Supplier',
            contact_person='Gautam',
            phone='+91 98888 22222',
            status='active'
        )
        self.category = ProductCategory.objects.create(name='Pantry')
        self.product = Product.objects.create(
            name='Fortune Sunflower Oil (15L Tin)',
            sku='TEST-OIL-015',
            category=self.category,
            standard_unit='tin',
            min_stock_alert=Decimal('5.00')
        )

        # Set initial stock of 2 tins
        StockItem.objects.create(
            user=self.retailer,
            product=self.product,
            current_stock=Decimal('2.00'),
            low_stock_threshold=Decimal('5.00')
        )

    def test_receive_purchase_order_updates_inventory_atomically(self):
        # Create a shipped PO
        po = PurchaseOrder.objects.create(
            po_number='PO-INV-001',
            retailer=self.retailer,
            supplier=self.supplier,
            status='shipped',
            total_amount=Decimal('18500.00'),
            is_inventory_stocked=False
        )
        item = PurchaseOrderItem.objects.create(
            purchase_order=po,
            product=self.product,
            quantity_ordered=Decimal('10.00'),
            unit='tin',
            unit_price=Decimal('1850.00'),
            item_total=Decimal('18500.00')
        )

        # Receive 10 units (no discrepancy)
        receive_payload = {
            'items': [
                {
                    'item_id': item.id,
                    'quantity_received': 10,
                    'quantity_damaged': 0,
                    'discrepancy_notes': 'All good'
                }
            ],
            'notes': 'Received in store'
        }

        resp = self.client.post(f'/api/v1/purchasing/{po.id}/receive/', receive_payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 'received')
        self.assertTrue(resp.data['is_inventory_stocked'])

        # Verify stock incremented: initial 2 + received 10 = 12
        stock = StockItem.objects.get(user=self.retailer, product=self.product)
        self.assertEqual(stock.current_stock, Decimal('12.00'))

        # Verify movement ledger
        movement = StockMovement.objects.filter(user=self.retailer, product=self.product, reference_id='PO-INV-001').first()
        self.assertIsNotNone(movement)
        self.assertEqual(movement.movement_type, 'purchase_receipt')
        self.assertEqual(movement.quantity_delta, Decimal('10.00'))
        self.assertEqual(movement.resulting_stock, Decimal('12.00'))

    def test_idempotent_duplicate_receipt_rejection(self):
        po = PurchaseOrder.objects.create(
            po_number='PO-INV-002',
            retailer=self.retailer,
            supplier=self.supplier,
            status='received',
            total_amount=Decimal('18500.00'),
            is_inventory_stocked=True # Already stocked!
        )
        item = PurchaseOrderItem.objects.create(
            purchase_order=po,
            product=self.product,
            quantity_ordered=Decimal('10.00'),
            unit='tin',
            unit_price=Decimal('1850.00'),
            item_total=Decimal('18500.00')
        )

        receive_payload = {
            'items': [{'item_id': item.id, 'quantity_received': 10}]
        }
        # Second attempt must be rejected and stock must NOT increase
        resp = self.client.post(f'/api/v1/purchasing/{po.id}/receive/', receive_payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already been received", resp.data['error'])

        # Stock must remain unchanged at 2.00
        stock = StockItem.objects.get(user=self.retailer, product=self.product)
        self.assertEqual(stock.current_stock, Decimal('2.00'))

    def test_manual_stock_adjustment_endpoint(self):
        payload = {
            'product_id': self.product.id,
            'new_quantity': 25.00,
            'reason': 'adjustment_add',
            'notes': 'Physical recount revealed more stock'
        }
        resp = self.client.post('/api/v1/inventory/adjust/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        stock = StockItem.objects.get(user=self.retailer, product=self.product)
        self.assertEqual(stock.current_stock, Decimal('25.00'))

        movement = StockMovement.objects.filter(user=self.retailer, product=self.product, reference_id='MANUAL_ADJUSTMENT').first()
        self.assertIsNotNone(movement)
        self.assertEqual(movement.quantity_delta, Decimal('23.00')) # 25 - 2
