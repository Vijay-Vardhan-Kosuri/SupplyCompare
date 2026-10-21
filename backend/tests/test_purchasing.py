from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from apps.accounts.models import User, RetailerProfile
from apps.catalog.models import ProductCategory, Product
from apps.suppliers.models import Supplier
from apps.quotations.models import Quotation
from apps.purchasing.models import PurchaseOrder, PurchaseOrderItem
from apps.accounts.authentication import generate_tokens_for_user

class PurchaseOrderWorkflowTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Users
        self.retailer = User.objects.create_user(
            email='po_retailer@supplycompare.local',
            password='TestPassword123',
            role='retailer'
        )
        RetailerProfile.objects.create(user=self.retailer, shop_name='PO Retail Store')
        token = generate_tokens_for_user(self.retailer)['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Supplier & Product
        self.supplier = Supplier.objects.create(
            name='Procurement Supplier Hub',
            contact_person='Ramesh',
            phone='+91 99999 11111',
            status='active'
        )
        self.category = ProductCategory.objects.create(name='Grains')
        self.product = Product.objects.create(
            name='Sharbati Wheat Flour (10kg)',
            sku='TEST-WHT-010',
            category=self.category,
            standard_unit='bag'
        )

        # Quotation
        self.quotation = Quotation.objects.create(
            supplier=self.supplier,
            product=self.product,
            quoted_unit='bag',
            unit_price=Decimal('420.00'),
            moq=Decimal('10.00'),
            available_stock=Decimal('100.00'),
            delivery_charge=Decimal('150.00'),
            expected_delivery_days=2,
            valid_until=timezone.now().date() + timedelta(days=20),
            status='active'
        )

    def test_create_po_from_quotation(self):
        payload = {
            'quotation_id': self.quotation.id,
            'quantity': 20,
            'delivery_address': 'Store Gate 2, Hyderabad',
            'notes': 'Deliver before 5 PM'
        }
        response = self.client.post('/api/v1/purchasing/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'draft')
        self.assertEqual(float(response.data['subtotal']), 8400.00) # 20 * 420
        self.assertEqual(float(response.data['delivery_charge']), 150.00)
        self.assertEqual(float(response.data['total_amount']), 8550.00)

        # Check Item was created
        po_id = response.data['id']
        po = PurchaseOrder.objects.get(id=po_id)
        self.assertEqual(po.items.count(), 1)
        self.assertEqual(po.items.first().quantity_ordered, Decimal('20.00'))

    def test_state_machine_valid_transitions(self):
        po = PurchaseOrder.objects.create(
            po_number='PO-TEST-001',
            retailer=self.retailer,
            supplier=self.supplier,
            status='draft',
            total_amount=Decimal('8550.00')
        )

        # draft -> submitted
        resp = self.client.post(f'/api/v1/purchasing/{po.id}/transition/', {'status': 'submitted'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        po.refresh_from_db()
        self.assertEqual(po.status, 'submitted')

        # submitted -> confirmed
        resp = self.client.post(f'/api/v1/purchasing/{po.id}/transition/', {'status': 'confirmed'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        po.refresh_from_db()
        self.assertEqual(po.status, 'confirmed')

        # confirmed -> shipped
        resp = self.client.post(f'/api/v1/purchasing/{po.id}/transition/', {'status': 'shipped'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        po.refresh_from_db()
        self.assertEqual(po.status, 'shipped')

    def test_state_machine_invalid_transition_rejected(self):
        po = PurchaseOrder.objects.create(
            po_number='PO-TEST-002',
            retailer=self.retailer,
            supplier=self.supplier,
            status='draft'
        )

        # draft -> shipped (invalid skip!)
        resp = self.client.post(f'/api/v1/purchasing/{po.id}/transition/', {'status': 'shipped'})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot transition order", resp.data['error'])

    def test_pdf_export_endpoint(self):
        po = PurchaseOrder.objects.create(
            po_number='PO-TEST-003',
            retailer=self.retailer,
            supplier=self.supplier,
            status='submitted',
            subtotal=Decimal('4200.00'),
            total_amount=Decimal('4350.00')
        )
        PurchaseOrderItem.objects.create(
            purchase_order=po,
            product=self.product,
            quantity_ordered=Decimal('10.00'),
            unit='bag',
            unit_price=Decimal('420.00'),
            item_total=Decimal('4200.00')
        )

        resp = self.client.get(f'/api/v1/purchasing/{po.id}/pdf/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp['Content-Type'], 'application/pdf')
        self.assertGreater(len(resp.content), 1000)
