from django.test import TestCase
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from apps.catalog.models import ProductCategory, Product, UnitConversion
from apps.suppliers.models import Supplier
from apps.quotations.models import Quotation
from apps.comparison.services import ComparisonService

class QuotationComparisonEngineTests(TestCase):
    def setUp(self):
        # 1. Category & Product
        self.category = ProductCategory.objects.create(name='Snacks & Biscuits')
        self.product = Product.objects.create(
            name='Parle-G Gold Biscuits (Carton of 24 Packs)',
            sku='TEST-BSC-PRL-024',
            category=self.category,
            standard_unit='carton'
        )

        # 2. Setup Suppliers A & B from Prompt
        self.supplier_a = Supplier.objects.create(
            name='Supplier A - Singhania Corp',
            contact_person='Vikram Singhania',
            phone='+91 98490 11111',
            city='Hyderabad',
            delivery_lead_days=2,
            rating=Decimal('4.80'),
            status='active'
        )

        self.supplier_b = Supplier.objects.create(
            name='Supplier B - Balaji Distributors',
            contact_person='Suresh Agarwal',
            phone='+91 93910 22222',
            city='Hyderabad',
            delivery_lead_days=1,
            rating=Decimal('4.60'),
            status='active'
        )

        today = timezone.now().date()
        future_date = today + timedelta(days=30)

        # Quotation A: ₹900 per carton, Free delivery (0), MOQ = 5 cartons, stock = 100
        self.quote_a = Quotation.objects.create(
            supplier=self.supplier_a,
            product=self.product,
            quoted_unit='carton',
            unit_price=Decimal('900.00'),
            moq=Decimal('5.00'),
            available_stock=Decimal('100.00'),
            delivery_charge=Decimal('0.00'),
            free_delivery_threshold=Decimal('0.00'),
            expected_delivery_days=2,
            valid_until=future_date,
            status='active'
        )

        # Quotation B: ₹870 per carton, ₹300 delivery, MOQ = 15 cartons, stock = 100
        self.quote_b = Quotation.objects.create(
            supplier=self.supplier_b,
            product=self.product,
            quoted_unit='carton',
            unit_price=Decimal('870.00'),
            moq=Decimal('15.00'),
            available_stock=Decimal('100.00'),
            delivery_charge=Decimal('300.00'),
            free_delivery_threshold=Decimal('0.00'),
            expected_delivery_days=1,
            valid_until=future_date,
            status='active'
        )

    def test_prompt_benchmark_for_10_cartons(self):
        """
        Prompt Test 1: For a request of 10 cartons:
        - Supplier A is eligible. Total = ₹9,000.
        - Supplier B is not eligible because the minimum is 15 cartons.
        - Recommended best deal must be Supplier A (Total ₹9,000).
        """
        res = ComparisonService.compare_quotations(
            product_id=self.product.id,
            requested_quantity=10,
            requested_unit='carton'
        )

        self.assertEqual(res['summary']['eligible_count'], 1)
        self.assertEqual(res['summary']['ineligible_count'], 1)

        # Supplier A verification
        eligible = res['eligible_suppliers']
        self.assertEqual(len(eligible), 1)
        sup_a_result = eligible[0]
        self.assertEqual(sup_a_result['supplier_name'], self.supplier_a.name)
        self.assertEqual(sup_a_result['total_cost'], 9000.00)
        self.assertTrue(sup_a_result['is_best_deal'])

        # Supplier B verification
        ineligible = res['ineligible_suppliers']
        self.assertEqual(len(ineligible), 1)
        sup_b_result = ineligible[0]
        self.assertEqual(sup_b_result['supplier_name'], self.supplier_b.name)
        self.assertFalse(sup_b_result['is_eligible'])
        self.assertIn("Minimum order is 15", sup_b_result['exclusion_reason'])

    def test_prompt_benchmark_for_15_cartons(self):
        """
        Prompt Test 2: For a request of 15 cartons:
        - Supplier A total = ₹13,500. (15 * 900 + 0)
        - Supplier B total = ₹13,350. (15 * 870 + 300)
        - Both are eligible, but Supplier B must be recommended as Best Deal!
        """
        res = ComparisonService.compare_quotations(
            product_id=self.product.id,
            requested_quantity=15,
            requested_unit='carton'
        )

        self.assertEqual(res['summary']['eligible_count'], 2)
        self.assertEqual(res['summary']['ineligible_count'], 0)

        eligible = res['eligible_suppliers']
        # Must be ranked by lowest total cost: Supplier B (13,350) before Supplier A (13,500)
        best = eligible[0]
        runner_up = eligible[1]

        self.assertEqual(best['supplier_name'], self.supplier_b.name)
        self.assertEqual(best['total_cost'], 13350.00)
        self.assertTrue(best['is_best_deal'])

        self.assertEqual(runner_up['supplier_name'], self.supplier_a.name)
        self.assertEqual(runner_up['total_cost'], 13500.00)
        self.assertFalse(runner_up['is_best_deal'])

        # Potential savings = 13,500 - 13,350 = 150
        self.assertEqual(res['summary']['potential_savings'], 150.00)

    def test_stock_availability_exclusion(self):
        """
        If requested quantity exceeds supplier stock, supplier must be flagged ineligible.
        """
        res = ComparisonService.compare_quotations(
            product_id=self.product.id,
            requested_quantity=120, # More than 100 stock
            requested_unit='carton'
        )
        self.assertEqual(res['summary']['eligible_count'], 0)
        self.assertEqual(res['summary']['ineligible_count'], 2)
        for inel in res['ineligible_suppliers']:
            self.assertIn("Insufficient stock", inel['exclusion_reason'])

    def test_quotation_expiry_exclusion(self):
        """
        Expired quotations must be rejected from eligible comparisons.
        """
        self.quote_a.status = 'expired'
        self.quote_a.save()

        res = ComparisonService.compare_quotations(
            product_id=self.product.id,
            requested_quantity=10,
            requested_unit='carton'
        )
        self.assertEqual(res['summary']['eligible_count'], 0)
        ineligible_a = [q for q in res['ineligible_suppliers'] if q['supplier_id'] == self.supplier_a.id][0]
        self.assertIn("inactive", ineligible_a['exclusion_reason'])

    def test_unit_conversion_comparison(self):
        """
        If quote is in cartons and requested quantity is in packets (1 carton = 24 packets).
        240 packets = 10 cartons.
        """
        UnitConversion.objects.create(
            product=self.product,
            from_unit='packet',
            to_unit='carton',
            conversion_factor=Decimal('0.0416666667') # 1/24
        )
        # Or from_unit='carton', to_unit='packet', factor=24
        UnitConversion.objects.filter(product=self.product).delete()
        UnitConversion.objects.create(
            product=self.product,
            from_unit='carton',
            to_unit='packet',
            conversion_factor=Decimal('24.00')
        )

        res = ComparisonService.compare_quotations(
            product_id=self.product.id,
            requested_quantity=240, # 240 packets = 10 cartons
            requested_unit='packet'
        )
        self.assertEqual(res['summary']['eligible_count'], 1)
        sup_a = res['eligible_suppliers'][0]
        self.assertEqual(sup_a['total_cost'], 9000.00)
