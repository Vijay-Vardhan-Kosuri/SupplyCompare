from django.db import models
from django.utils import timezone
from apps.suppliers.models import Supplier
from apps.catalog.models import Product

class Quotation(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('archived', 'Archived'),
    )

    DISCOUNT_TYPE_CHOICES = (
        ('none', 'No Discount'),
        ('flat', 'Flat Amount Discount (₹)'),
        ('percentage', 'Percentage Discount (%)'),
    )

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='quotations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='quotations')
    quoted_unit = models.CharField(max_length=30, default='piece', help_text="Unit in which price is quoted, e.g. carton, bag, kg, piece")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Price per quoted unit in INR")
    moq = models.DecimalField(max_digits=10, decimal_places=2, default=1.00, help_text="Minimum Order Quantity in quoted unit")
    available_stock = models.DecimalField(max_digits=10, decimal_places=2, default=9999.00, help_text="Supplier available stock in quoted unit")
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Fixed delivery charge in INR")
    free_delivery_threshold = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Order amount above which delivery is free (0 if no free delivery)")
    expected_delivery_days = models.PositiveIntegerField(default=2, help_text="Expected delivery lead time in days")
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='none')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Tax / GST percentage (0%, 5%, 12%, 18%)")
    valid_until = models.DateField(help_text="Expiry date for quotation pricing and terms")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    notes = models.TextField(blank=True, help_text="Special terms, payment conditions, or brand details")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quotations'
        verbose_name = 'Supplier Quotation'
        verbose_name_plural = 'Supplier Quotations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.supplier.name} - {self.product.name}: ₹{self.unit_price}/{self.quoted_unit}"

    @property
    def is_expired(self):
        if self.status == 'expired':
            return True
        return self.valid_until < timezone.now().date()

    @property
    def is_currently_valid(self):
        return self.status == 'active' and not self.is_expired and self.supplier.status == 'active'
