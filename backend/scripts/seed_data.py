import os
import sys
import django
from decimal import Decimal
from datetime import timedelta

# Ensure python path includes backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

django.setup()

from django.utils import timezone
from apps.accounts.models import User, RetailerProfile, SupplierProfile
from apps.catalog.models import ProductCategory, Product, UnitConversion
from apps.suppliers.models import Supplier, SupplierContact
from apps.quotations.models import Quotation
from apps.purchasing.models import PurchaseOrder, PurchaseOrderItem, PurchaseOrderHistory
from apps.inventory.models import StockItem, StockMovement
from apps.notifications.models import Notification

def seed():
    print("🌱 Starting SupplyCompare Database Seeding...")

    # 1. Accounts
    admin_user, _ = User.objects.get_or_create(
        email='admin@supplycompare.local',
        defaults={
            'first_name': 'Platform',
            'last_name': 'Administrator',
            'phone': '+91 98765 00001',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    admin_user.set_password('Admin@123')
    admin_user.save()

    retailer_user, _ = User.objects.get_or_create(
        email='retailer@supplycompare.local',
        defaults={
            'first_name': 'Ramesh',
            'last_name': 'Gupta',
            'phone': '+91 98765 11111',
            'role': 'retailer',
        }
    )
    retailer_user.set_password('Retailer@123')
    retailer_user.save()

    retailer_profile, _ = RetailerProfile.objects.get_or_create(
        user=retailer_user,
        defaults={
            'shop_name': 'Sri Lakshmi Kirana & General Stores',
            'gstin': '36AAACR1234M1Z5',
            'shop_type': 'kirana',
            'address_line': 'Plot 42, Main Road, KPHB Colony',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'pincode': '500072',
            'currency': 'INR'
        }
    )

    supplier_user, _ = User.objects.get_or_create(
        email='supplier@supplycompare.local',
        defaults={
            'first_name': 'Vikram',
            'last_name': 'Singhania',
            'phone': '+91 98765 22222',
            'role': 'supplier',
        }
    )
    supplier_user.set_password('Supplier@123')
    supplier_user.save()

    supplier_profile, _ = SupplierProfile.objects.get_or_create(
        user=supplier_user,
        defaults={
            'business_name': 'Singhania Wholesale Agri Corp',
            'designation': 'Regional Managing Director',
            'is_verified': True
        }
    )

    print("✔ Accounts seeded (Admin, Retailer, Supplier)")

    # 2. Product Categories
    categories_data = [
        ('Staples & Grains', 'staples-grains', 'Rice, Atta, Pulses, Millets, and Grain essentials', 'Wheat'),
        ('Edible Oils & Ghee', 'edible-oils', 'Mustard oil, Sunflower oil, Groundnut oil, Pure Cow Ghee', 'Droplet'),
        ('Spices & Seasonings', 'spices-seasonings', 'Whole and powdered spices, masalas, turmeric, cumin', 'Flame'),
        ('Dairy & Bakery', 'dairy-bakery', 'Milk cartons, butter, cheese, sliced breads, rusks', 'Cookie'),
        ('Packaged Foods & Snacks', 'packaged-snacks', 'Biscuits, noodles, breakfast cereals, namkeen, pasta', 'PackageCheck'),
        ('Beverages & Tea', 'beverages-tea', 'Premium Assam tea leaves, roast coffee, malt drinks', 'Coffee'),
        ('Personal Care & Cleaning', 'personal-cleaning', 'Detergent bars, toilet soaps, floor cleaner liquids', 'Sparkles'),
    ]

    cat_map = {}
    for name, slug, desc, icon in categories_data:
        cat, _ = ProductCategory.objects.get_or_create(
            name=name,
            defaults={'slug': slug, 'description': desc, 'icon_name': icon}
        )
        cat_map[name] = cat
    print(f"✔ {len(cat_map)} Categories created")

    # 3. Suppliers
    suppliers_data = [
        {
            'name': 'Singhania Wholesale Agri Corp',
            'gstin': '36AAACS4567P1Z2',
            'contact_person': 'Vikram Singhania',
            'phone': '+91 98490 12345',
            'email': 'orders@singhaniawholesale.in',
            'address': 'D-14, Agricultural Market Yard, Bowenpally',
            'city': 'Secunderabad',
            'state': 'Telangana',
            'payment_terms': 'net_15',
            'delivery_lead_days': 2,
            'rating': 4.8,
            'categories': ['Staples & Grains', 'Edible Oils & Ghee']
        },
        {
            'name': 'Sri Venkateshwara Traders',
            'gstin': '36ABCTV7890K1Z9',
            'contact_person': 'K. Venkat Rao',
            'phone': '+91 94401 56789',
            'email': 'sales@svtwholesale.com',
            'address': 'Shop 88, General Bazar, Ranigunj',
            'city': 'Secunderabad',
            'state': 'Telangana',
            'payment_terms': 'net_30',
            'delivery_lead_days': 3,
            'rating': 4.5,
            'categories': ['Staples & Grains', 'Spices & Seasonings']
        },
        {
            'name': 'Balaji FMCG Distributors',
            'gstin': '36AAGCB1122J1Z3',
            'contact_person': 'Suresh Agarwal',
            'phone': '+91 93910 88990',
            'email': 'info@balajidistributors.net',
            'address': 'Warehouse Complex 5, Kukatpally Industrial Area',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'payment_terms': 'cod',
            'delivery_lead_days': 1,
            'rating': 4.9,
            'categories': ['Packaged Foods & Snacks', 'Beverages & Tea', 'Personal Care & Cleaning']
        },
        {
            'name': 'Deccan Oil & Grain Mills',
            'gstin': '36AADCD3344M1Z4',
            'contact_person': 'Mohd. Rizwan',
            'phone': '+91 98850 77112',
            'email': 'orders@deccanoils.com',
            'address': 'Plot 12, IDA Nacharam',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'payment_terms': 'net_7',
            'delivery_lead_days': 2,
            'rating': 4.3,
            'categories': ['Edible Oils & Ghee', 'Staples & Grains']
        },
        {
            'name': 'Telangana Spice & Agro Exports',
            'gstin': '36AAHCT5566N1Z1',
            'contact_person': 'Anand Reddy',
            'phone': '+91 97010 33445',
            'email': 'anand@tsspiceagro.com',
            'address': 'Kothapet Wholesale Complex',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'payment_terms': 'advance',
            'delivery_lead_days': 4,
            'rating': 4.2,
            'categories': ['Spices & Seasonings']
        },
        {
            'name': 'Krishna Dairy & Cold Chain Supplies',
            'gstin': '36AAFCK7788R1Z8',
            'contact_person': 'P. Krishna Murthy',
            'phone': '+91 98661 22334',
            'email': 'dispatch@krishnadairy.co.in',
            'address': 'Phase 2, Cherlapally Industrial Estate',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'payment_terms': 'cod',
            'delivery_lead_days': 1,
            'rating': 4.7,
            'categories': ['Dairy & Bakery']
        },
        {
            'name': 'Golden Harvest FMCG Hub',
            'gstin': '36AABCG9900L1Z6',
            'contact_person': 'Gautam Mehra',
            'phone': '+91 99590 66778',
            'email': 'supply@goldenharvesthub.in',
            'address': 'Survey 118, Medchal Highway Logistics Park',
            'city': 'Medchal',
            'state': 'Telangana',
            'payment_terms': 'net_15',
            'delivery_lead_days': 2,
            'rating': 4.6,
            'categories': ['Packaged Foods & Snacks', 'Beverages & Tea']
        },
        {
            'name': 'Metro Clean Hygiene Wholesalers',
            'gstin': '36AAECM2233Q1Z7',
            'contact_person': 'Naveen Kumar',
            'phone': '+91 91210 44556',
            'email': 'metroclean@hyderabadgoods.com',
            'address': 'Shed 9, Auto Nagar',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'payment_terms': 'net_30',
            'delivery_lead_days': 3,
            'rating': 4.4,
            'categories': ['Personal Care & Cleaning']
        }
    ]

    sup_map = {}
    for s_info in suppliers_data:
        cat_names = s_info.pop('categories')
        sup, _ = Supplier.objects.get_or_create(
            name=s_info['name'],
            defaults=s_info
        )
        for cn in cat_names:
            if cn in cat_map:
                sup.categories.add(cat_map[cn])
        sup_map[sup.name] = sup

    # Link the supplier user profile to the first supplier entity
    supplier_profile.supplier_id = sup_map['Singhania Wholesale Agri Corp'].id
    supplier_profile.save()
    print(f"✔ {len(sup_map)} Suppliers created & linked")

    # 4. Products Catalog
    products_data = [
        # Staples & Grains
        {
            'name': 'India Gate Basmati Rice Classic (10kg Bag)',
            'sku': 'RICE-BAS-001',
            'category': 'Staples & Grains',
            'brand': 'India Gate',
            'standard_unit': 'bag',
            'min_stock_alert': Decimal('15'),
            'target_purchase_price': Decimal('890.00'),
            'description': 'Premium aged long-grain basmati rice suitable for biryani and pulao.'
        },
        {
            'name': 'Aashirvaad Shudh Chakki Atta (10kg Bag)',
            'sku': 'ATTA-AAS-001',
            'category': 'Staples & Grains',
            'brand': 'Aashirvaad',
            'standard_unit': 'bag',
            'min_stock_alert': Decimal('20'),
            'target_purchase_price': Decimal('420.00'),
            'description': '100% whole wheat flour with dietary fiber.'
        },
        {
            'name': 'Tata Sampann Unpolished Toor Dal (1kg)',
            'sku': 'DAL-TOR-001',
            'category': 'Staples & Grains',
            'brand': 'Tata Sampann',
            'standard_unit': 'packet',
            'min_stock_alert': Decimal('30'),
            'target_purchase_price': Decimal('145.00'),
            'description': 'Unpolished, pesticide-tested pigeon pea dal rich in protein.'
        },
        {
            'name': 'Fortune Sugar M-30 Fine Granules (50kg Bag)',
            'sku': 'SUG-M30-050',
            'category': 'Staples & Grains',
            'brand': 'Fortune',
            'standard_unit': 'bag',
            'min_stock_alert': Decimal('5'),
            'target_purchase_price': Decimal('2100.00'),
            'description': 'Sulphur-free refined crystalline cane sugar.'
        },

        # Edible Oils & Ghee
        {
            'name': 'Fortune Sunlite Refined Sunflower Oil (15L Tin)',
            'sku': 'OIL-SUN-015',
            'category': 'Edible Oils & Ghee',
            'brand': 'Fortune',
            'standard_unit': 'tin',
            'min_stock_alert': Decimal('8'),
            'target_purchase_price': Decimal('1850.00'),
            'description': 'Refined cooking sunflower oil fortified with vitamins A and D.'
        },
        {
            'name': 'Dhara Kachi Ghani Mustard Oil (1L Pouch)',
            'sku': 'OIL-MUS-001',
            'category': 'Edible Oils & Ghee',
            'brand': 'Dhara',
            'standard_unit': 'packet',
            'min_stock_alert': Decimal('40'),
            'target_purchase_price': Decimal('132.00'),
            'description': 'Cold pressed pungent mustard cooking oil.'
        },
        {
            'name': 'Amul Pure Cow Ghee (1L Tin)',
            'sku': 'GHEE-AML-001',
            'category': 'Edible Oils & Ghee',
            'brand': 'Amul',
            'standard_unit': 'tin',
            'min_stock_alert': Decimal('12'),
            'target_purchase_price': Decimal('610.00'),
            'description': 'Traditional granulated pure cow ghee with rich natural aroma.'
        },

        # Spices
        {
            'name': 'Everest Tikhalal Chilli Powder (500g)',
            'sku': 'SPC-EVE-001',
            'category': 'Spices & Seasonings',
            'brand': 'Everest',
            'standard_unit': 'packet',
            'min_stock_alert': Decimal('25'),
            'target_purchase_price': Decimal('185.00'),
            'description': 'Hot and bright red pungent ground red pepper.'
        },
        {
            'name': 'Catch Turmeric Powder Haldi (500g)',
            'sku': 'SPC-CAT-002',
            'category': 'Spices & Seasonings',
            'brand': 'Catch',
            'standard_unit': 'packet',
            'min_stock_alert': Decimal('25'),
            'target_purchase_price': Decimal('115.00'),
            'description': 'High-curcumin ground golden turmeric root.'
        },

        # Packaged Snacks & Biscuits
        {
            'name': 'Parle-G Gold Glucose Biscuits (Carton of 24 Packs)',
            'sku': 'BSC-PRL-024',
            'category': 'Packaged Foods & Snacks',
            'brand': 'Parle',
            'standard_unit': 'carton',
            'min_stock_alert': Decimal('10'),
            'target_purchase_price': Decimal('880.00'),
            'description': 'Wholesale master shipper of 24 consumer packs of 250g glucose biscuits.'
        },
        {
            'name': 'Maggi 2-Minute Masala Noodles (Carton of 96 units)',
            'sku': 'NDL-MAG-096',
            'category': 'Packaged Foods & Snacks',
            'brand': 'Nestle Maggi',
            'standard_unit': 'carton',
            'min_stock_alert': Decimal('6'),
            'target_purchase_price': Decimal('1250.00'),
            'description': 'Standard retailer master case containing 96 single 70g packs.'
        },

        # Beverages
        {
            'name': 'Red Label Leaf Tea (1kg Pack)',
            'sku': 'TEA-BRO-001',
            'category': 'Beverages & Tea',
            'brand': 'Brooke Bond Red Label',
            'standard_unit': 'packet',
            'min_stock_alert': Decimal('20'),
            'target_purchase_price': Decimal('440.00'),
            'description': 'Strong Assam CTC black tea blend for rich kadak chai.'
        },

        # Personal Care & Cleaning
        {
            'name': 'Surf Excel Quick Wash Detergent Powder (1kg)',
            'sku': 'DET-SUR-001',
            'category': 'Personal Care & Cleaning',
            'brand': 'Surf Excel',
            'standard_unit': 'packet',
            'min_stock_alert': Decimal('30'),
            'target_purchase_price': Decimal('135.00'),
            'description': 'Heavy-duty enzymatic laundry powder with stain remover.'
        },
        {
            'name': 'Dettol Original Bathing Soap (Carton of 48 Bars)',
            'sku': 'SOP-DET-048',
            'category': 'Personal Care & Cleaning',
            'brand': 'Dettol',
            'standard_unit': 'carton',
            'min_stock_alert': Decimal('5'),
            'target_purchase_price': Decimal('1680.00'),
            'description': 'Master shipper carton of 48 individual antibacterial 125g soap cakes.'
        }
    ]

    prod_map = {}
    for p_info in products_data:
        cat_name = p_info.pop('category')
        cat = cat_map[cat_name]
        prod, _ = Product.objects.get_or_create(
            sku=p_info['sku'],
            defaults={**p_info, 'category': cat}
        )
        prod_map[prod.sku] = prod
    print(f"✔ {len(prod_map)} Catalog Products created")

    # 5. Unit Conversions
    conversions = [
        # 1 carton of Parle-G = 24 packets
        (prod_map['BSC-PRL-024'], 'carton', 'packet', Decimal('24.00'), '1 wholesale carton has 24 packets'),
        # 1 carton of Maggi = 96 packets
        (prod_map['NDL-MAG-096'], 'carton', 'packet', Decimal('96.00'), '1 master case has 96 packets'),
        # 1 carton of Dettol = 48 bars
        (prod_map['SOP-DET-048'], 'carton', 'piece', Decimal('48.00'), '1 carton has 48 soap bars'),
        # Global conversions
        (None, 'quintal', 'kg', Decimal('100.00'), '1 quintal is 100 kg'),
        (None, 'kg', 'g', Decimal('1000.00'), '1 kilogram is 1000 grams'),
        (None, 'litre', 'ml', Decimal('1000.00'), '1 litre is 1000 millilitres'),
        (None, 'dozen', 'piece', Decimal('12.00'), '1 dozen is 12 units'),
    ]

    for p, fu, tu, factor, note in conversions:
        UnitConversion.objects.get_or_create(
            product=p, from_unit=fu, to_unit=tu,
            defaults={'conversion_factor': factor, 'notes': note}
        )
    print("✔ Unit conversion matrix configured")

    # 6. Quotations
    # NOTE: Include the exact verification scenario from Prompt 4.D:
    # "Supplier A charges ₹900 per carton with free delivery and a minimum order of 5 cartons.
    #  Supplier B charges ₹870 per carton plus ₹300 delivery with a minimum order of 15 cartons."
    # Let's map this directly to Parle-G cartons:
    today = timezone.now().date()
    future_date = today + timedelta(days=45)
    past_date = today - timedelta(days=10)

    parle_g = prod_map['BSC-PRL-024']
    sup_singhania = sup_map['Singhania Wholesale Agri Corp']
    sup_balaji = sup_map['Balaji FMCG Distributors']
    sup_golden = sup_map['Golden Harvest FMCG Hub']

    # Prompt Test Case:
    # Supplier A (Singhania): ₹900/carton, free delivery (0 delivery charge), MOQ 5
    Quotation.objects.create(
        supplier=sup_singhania,
        product=parle_g,
        quoted_unit='carton',
        unit_price=Decimal('900.00'),
        moq=Decimal('5.00'),
        available_stock=Decimal('100.00'),
        delivery_charge=Decimal('0.00'),
        free_delivery_threshold=Decimal('0.00'),
        expected_delivery_days=2,
        discount_type='none',
        tax_percentage=Decimal('0.00'),
        valid_until=future_date,
        status='active',
        notes='Free express doorstep delivery for kirana retailers. MOQ 5 cartons.'
    )

    # Supplier B (Balaji FMCG): ₹870/carton, delivery ₹300, MOQ 15
    Quotation.objects.create(
        supplier=sup_balaji,
        product=parle_g,
        quoted_unit='carton',
        unit_price=Decimal('870.00'),
        moq=Decimal('15.00'),
        available_stock=Decimal('150.00'),
        delivery_charge=Decimal('300.00'),
        free_delivery_threshold=Decimal('0.00'),
        expected_delivery_days=1,
        discount_type='none',
        tax_percentage=Decimal('0.00'),
        valid_until=future_date,
        status='active',
        notes='Wholesale bulk rate ₹870/carton with ₹300 flat logistics charge. MOQ 15 cartons.'
    )

    # Supplier C (Golden Harvest): ₹920/carton, delivery ₹150, MOQ 2, but has 5% discount
    Quotation.objects.create(
        supplier=sup_golden,
        product=parle_g,
        quoted_unit='carton',
        unit_price=Decimal('920.00'),
        moq=Decimal('2.00'),
        available_stock=Decimal('80.00'),
        delivery_charge=Decimal('150.00'),
        free_delivery_threshold=Decimal('5000.00'),
        expected_delivery_days=3,
        discount_type='percentage',
        discount_value=Decimal('5.00'),
        tax_percentage=Decimal('0.00'),
        valid_until=future_date,
        status='active',
        notes='Flexible low MOQ tier with 5% discount on bill.'
    )

    # Expired quotation for testing filter
    Quotation.objects.create(
        supplier=sup_map['Sri Venkateshwara Traders'],
        product=parle_g,
        quoted_unit='carton',
        unit_price=Decimal('850.00'),
        moq=Decimal('10.00'),
        available_stock=Decimal('50.00'),
        delivery_charge=Decimal('200.00'),
        expected_delivery_days=3,
        valid_until=past_date,
        status='expired',
        notes='Old promotional batch price (expired).'
    )

    # Seed Quotations for other products to give rich data
    rice = prod_map['RICE-BAS-001']
    Quotation.objects.create(
        supplier=sup_singhania,
        product=rice,
        quoted_unit='bag',
        unit_price=Decimal('890.00'),
        moq=Decimal('10.00'),
        available_stock=Decimal('250.00'),
        delivery_charge=Decimal('250.00'),
        free_delivery_threshold=Decimal('15000.00'),
        expected_delivery_days=2,
        valid_until=future_date,
        status='active'
    )
    Quotation.objects.create(
        supplier=sup_map['Sri Venkateshwara Traders'],
        product=rice,
        quoted_unit='bag',
        unit_price=Decimal('865.00'),
        moq=Decimal('20.00'),
        available_stock=Decimal('180.00'),
        delivery_charge=Decimal('400.00'),
        expected_delivery_days=3,
        valid_until=future_date,
        status='active'
    )
    Quotation.objects.create(
        supplier=sup_map['Deccan Oil & Grain Mills'],
        product=rice,
        quoted_unit='bag',
        unit_price=Decimal('915.00'),
        moq=Decimal('5.00'),
        available_stock=Decimal('60.00'),
        delivery_charge=Decimal('0.00'),
        expected_delivery_days=1,
        valid_until=future_date,
        status='active'
    )

    # Atta quotations
    atta = prod_map['ATTA-AAS-001']
    Quotation.objects.create(
        supplier=sup_singhania,
        product=atta,
        quoted_unit='bag',
        unit_price=Decimal('415.00'),
        moq=Decimal('15.00'),
        available_stock=Decimal('300.00'),
        delivery_charge=Decimal('200.00'),
        expected_delivery_days=2,
        valid_until=future_date,
        status='active'
    )
    Quotation.objects.create(
        supplier=sup_map['Deccan Oil & Grain Mills'],
        product=atta,
        quoted_unit='bag',
        unit_price=Decimal('425.00'),
        moq=Decimal('10.00'),
        available_stock=Decimal('120.00'),
        delivery_charge=Decimal('150.00'),
        free_delivery_threshold=Decimal('8000.00'),
        expected_delivery_days=2,
        valid_until=future_date,
        status='active'
    )

    # Sunflower Oil quotations
    oil = prod_map['OIL-SUN-015']
    Quotation.objects.create(
        supplier=sup_singhania,
        product=oil,
        quoted_unit='tin',
        unit_price=Decimal('1840.00'),
        moq=Decimal('5.00'),
        available_stock=Decimal('75.00'),
        delivery_charge=Decimal('150.00'),
        expected_delivery_days=2,
        valid_until=future_date,
        status='active'
    )
    Quotation.objects.create(
        supplier=sup_map['Deccan Oil & Grain Mills'],
        product=oil,
        quoted_unit='tin',
        unit_price=Decimal('1810.00'),
        moq=Decimal('10.00'),
        available_stock=Decimal('120.00'),
        delivery_charge=Decimal('250.00'),
        expected_delivery_days=2,
        valid_until=future_date,
        status='active'
    )

    # Dettol soap quotations
    soap = prod_map['SOP-DET-048']
    Quotation.objects.create(
        supplier=sup_balaji,
        product=soap,
        quoted_unit='carton',
        unit_price=Decimal('1660.00'),
        moq=Decimal('3.00'),
        available_stock=Decimal('40.00'),
        delivery_charge=Decimal('100.00'),
        expected_delivery_days=1,
        valid_until=future_date,
        status='active'
    )
    Quotation.objects.create(
        supplier=sup_map['Metro Clean Hygiene Wholesalers'],
        product=soap,
        quoted_unit='carton',
        unit_price=Decimal('1640.00'),
        moq=Decimal('8.00'),
        available_stock=Decimal('60.00'),
        delivery_charge=Decimal('180.00'),
        expected_delivery_days=3,
        valid_until=future_date,
        status='active'
    )

    # Maggi noodles quotations
    maggi = prod_map['NDL-MAG-096']
    Quotation.objects.create(
        supplier=sup_balaji,
        product=maggi,
        quoted_unit='carton',
        unit_price=Decimal('1230.00'),
        moq=Decimal('4.00'),
        available_stock=Decimal('90.00'),
        delivery_charge=Decimal('120.00'),
        expected_delivery_days=1,
        valid_until=future_date,
        status='active'
    )
    Quotation.objects.create(
        supplier=sup_golden,
        product=maggi,
        quoted_unit='carton',
        unit_price=Decimal('1215.00'),
        moq=Decimal('10.00'),
        available_stock=Decimal('110.00'),
        delivery_charge=Decimal('200.00'),
        expected_delivery_days=2,
        valid_until=future_date,
        status='active'
    )

    print(f"✔ Quotations populated (including prompt verification benchmarks)")

    # 7. Purchase Orders & Receipts
    po1 = PurchaseOrder.objects.create(
        po_number='PO-2026-0001',
        retailer=retailer_user,
        supplier=sup_singhania,
        order_date=today - timedelta(days=12),
        expected_delivery_date=today - timedelta(days=10),
        actual_delivery_date=today - timedelta(days=10),
        status='received',
        subtotal=Decimal('17800.00'),
        discount_amount=Decimal('0.00'),
        delivery_charge=Decimal('0.00'),
        tax_amount=Decimal('0.00'),
        total_amount=Decimal('17800.00'),
        payment_terms='Net 15 Days',
        delivery_address='Plot 42, Main Road, KPHB Colony, Hyderabad',
        is_inventory_stocked=True,
        notes='Bulk order for Basmati Rice before festive rush.'
    )
    PurchaseOrderItem.objects.create(
        purchase_order=po1,
        product=rice,
        quantity_ordered=Decimal('20.00'),
        unit='bag',
        unit_price=Decimal('890.00'),
        quantity_received=Decimal('20.00'),
        quantity_damaged=Decimal('0.00'),
        item_total=Decimal('17800.00')
    )
    PurchaseOrderHistory.objects.create(
        purchase_order=po1,
        from_status='shipped',
        to_status='received',
        changed_by=retailer_user,
        notes='Full batch received and verified in good condition.'
    )

    # PO 2: In-Transit (Shipped)
    po2 = PurchaseOrder.objects.create(
        po_number='PO-2026-0002',
        retailer=retailer_user,
        supplier=sup_balaji,
        order_date=today - timedelta(days=2),
        expected_delivery_date=today + timedelta(days=1),
        status='shipped',
        subtotal=Decimal('8700.00'),
        discount_amount=Decimal('0.00'),
        delivery_charge=Decimal('300.00'),
        tax_amount=Decimal('0.00'),
        total_amount=Decimal('9000.00'),
        payment_terms='Cash on Delivery',
        delivery_address='Plot 42, Main Road, KPHB Colony, Hyderabad',
        is_inventory_stocked=False,
        notes='10 Cartons Parle-G Gold biscuits. Vehicle dispatched.'
    )
    PurchaseOrderItem.objects.create(
        purchase_order=po2,
        product=parle_g,
        quantity_ordered=Decimal('10.00'),
        unit='carton',
        unit_price=Decimal('870.00'),
        item_total=Decimal('8700.00')
    )

    # PO 3: Confirmed
    po3 = PurchaseOrder.objects.create(
        po_number='PO-2026-0003',
        retailer=retailer_user,
        supplier=sup_map['Deccan Oil & Grain Mills'],
        order_date=today - timedelta(days=1),
        expected_delivery_date=today + timedelta(days=2),
        status='confirmed',
        subtotal=Decimal('18100.00'),
        discount_amount=Decimal('0.00'),
        delivery_charge=Decimal('250.00'),
        tax_amount=Decimal('0.00'),
        total_amount=Decimal('18350.00'),
        payment_terms='Net 7 Days',
        delivery_address='Plot 42, Main Road, KPHB Colony, Hyderabad',
        is_inventory_stocked=False,
        notes='Sunflower Oil 15L Tins.'
    )
    PurchaseOrderItem.objects.create(
        purchase_order=po3,
        product=oil,
        quantity_ordered=Decimal('10.00'),
        unit='tin',
        unit_price=Decimal('1810.00'),
        item_total=Decimal('18100.00')
    )

    print("✔ Realistic Purchase Orders seeded")

    # 8. Inventory & Stock Items
    stock_items_data = [
        (rice, Decimal('25.00'), Decimal('15.00')),
        (atta, Decimal('8.00'), Decimal('20.00')),      # LOW STOCK!
        (oil, Decimal('5.00'), Decimal('8.00')),        # LOW STOCK!
        (parle_g, Decimal('12.00'), Decimal('10.00')),
        (maggi, Decimal('3.00'), Decimal('6.00')),       # LOW STOCK!
        (soap, Decimal('14.00'), Decimal('5.00')),
        (prod_map['TEA-BRO-001'], Decimal('28.00'), Decimal('20.00')),
        (prod_map['DET-SUR-001'], Decimal('35.00'), Decimal('30.00')),
        (prod_map['DAL-TOR-001'], Decimal('45.00'), Decimal('30.00')),
    ]

    for p, stock, thresh in stock_items_data:
        si, _ = StockItem.objects.get_or_create(
            user=retailer_user,
            product=p,
            defaults={
                'current_stock': stock,
                'low_stock_threshold': thresh,
                'last_restocked_at': timezone.now() - timedelta(days=10)
            }
        )
        StockMovement.objects.create(
            user=retailer_user,
            product=p,
            movement_type='purchase_receipt',
            quantity_delta=stock,
            unit=p.standard_unit,
            previous_stock=Decimal('0.00'),
            resulting_stock=stock,
            reference_id='INITIAL_STOCK',
            notes='Initial stock balance verified during audit'
        )
    print("✔ Inventory stock items and movements ledger initialized")

    # 9. In-app notifications
    notifications_data = [
        ("Purchase Order Shipped", "Supplier Balaji FMCG has dispatched order PO-2026-0002. Expected arrival tomorrow.", "order_status", "/purchase-orders"),
        ("Low Stock Alert: Aashirvaad Atta", "Current stock of Aashirvaad Atta is 8 bags, which is below your safety threshold of 20 bags.", "low_stock", "/inventory"),
        ("Low Stock Alert: Sunflower Oil", "Fortune Sunlite Oil is down to 5 tins. Compare active quotations now to reorder.", "low_stock", "/compare"),
        ("New Quotation Available", "Singhania Wholesale updated prices for India Gate Basmati Rice.", "system", "/quotations")
    ]
    for title, msg, n_type, link in notifications_data:
        Notification.objects.create(
            user=retailer_user,
            title=title,
            message=msg,
            notification_type=n_type,
            link_url=link
        )
    print("✔ Notifications created")

    print("\n🎉 DATABASE SEEDING COMPLETED SUCCESSFULLY!")
    print("==================================================")
    print("Demo Retailer Credentials:")
    print("  Email:    retailer@supplycompare.local")
    print("  Password: Retailer@123")
    print("Demo Supplier Credentials:")
    print("  Email:    supplier@supplycompare.local")
    print("  Password: Supplier@123")
    print("Demo Admin Credentials:")
    print("  Email:    admin@supplycompare.local")
    print("  Password: Admin@123")
    print("==================================================")

if __name__ == '__main__':
    seed()
