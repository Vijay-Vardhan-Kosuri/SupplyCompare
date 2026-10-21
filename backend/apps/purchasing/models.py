from django.db import models
from django.utils import timezone
from apps.accounts.models import User
from apps.suppliers.models import Supplier
from apps.catalog.models import Product
from apps.quotations.models import Quotation

class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted to Supplier'),
        ('confirmed', 'Confirmed by Supplier'),
        ('shipped', 'Shipped / In Transit'),
        ('received', 'Received & Stocked'),
        ('cancelled', 'Cancelled'),
    )

    # Valid state transitions
    VALID_TRANSITIONS = {
        'draft': ['submitted', 'cancelled'],
        'submitted': ['confirmed', 'cancelled'],
        'confirmed': ['shipped', 'cancelled'],
        'shipped': ['received', 'cancelled'],
        'received': [],    # Terminal state
        'cancelled': [],   # Terminal state
    }

    po_number = models.CharField(max_length=50, unique=True, db_index=True)
    retailer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_orders')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_orders')
    source_quotation = models.ForeignKey(Quotation, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_orders')

    order_date = models.DateField(default=timezone.localdate)
    expected_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    payment_terms = models.CharField(max_length=50, blank=True)
    delivery_address = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    is_inventory_stocked = models.BooleanField(default=False, help_text="Guard against duplicate stock addition")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'purchasing_orders'
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.po_number} - {self.supplier.name} ({self.get_status_display()})"

    def can_transition_to(self, new_status):
        return new_status in self.VALID_TRANSITIONS.get(self.status, [])

    @classmethod
    def generate_po_number(cls):
        year = timezone.now().year
        last_po = cls.objects.filter(po_number__startswith=f"PO-{year}").order_by('-id').first()
        if last_po and '-' in last_po.po_number:
            try:
                parts = last_po.po_number.split('-')
                seq = int(parts[-1]) + 1
            except (ValueError, IndexError):
                seq = cls.objects.count() + 1
        else:
            seq = cls.objects.count() + 1
        return f"PO-{year}-{seq:04d}"


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='po_items')
    quantity_ordered = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=30, default='piece')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity_damaged = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    item_total = models.DecimalField(max_digits=12, decimal_places=2)
    discrepancy_notes = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'purchasing_order_items'
        verbose_name = 'Purchase Order Item'
        verbose_name_plural = 'Purchase Order Items'

    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.product.name} ({self.quantity_ordered} {self.unit})"

    @property
    def has_discrepancy(self):
        return (self.quantity_received + self.quantity_damaged) != self.quantity_ordered


class PurchaseOrderHistory(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='history')
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'purchasing_order_history'
        verbose_name = 'Purchase Order History'
        verbose_name_plural = 'Purchase Order Histories'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.purchase_order.po_number}: {self.from_status} -> {self.to_status} at {self.timestamp}"
