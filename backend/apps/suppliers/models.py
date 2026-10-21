from django.db import models
from apps.catalog.models import ProductCategory

class Supplier(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    )

    PAYMENT_TERMS_CHOICES = (
        ('cod', 'Cash on Delivery (COD)'),
        ('advance', '100% Advance Payment'),
        ('net_7', 'Net 7 Days'),
        ('net_15', 'Net 15 Days'),
        ('net_30', 'Net 30 Days'),
        ('net_45', 'Net 45 Days'),
    )

    name = models.CharField(max_length=200, db_index=True)
    gstin = models.CharField(max_length=30, blank=True, help_text="GST / Tax Identification")
    contact_person = models.CharField(max_length=150)
    phone = models.CharField(max_length=30, db_index=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, default='Hyderabad')
    state = models.CharField(max_length=100, default='Telangana')
    pincode = models.CharField(max_length=20, blank=True)
    payment_terms = models.CharField(max_length=30, choices=PAYMENT_TERMS_CHOICES, default='net_15')
    delivery_lead_days = models.PositiveIntegerField(default=2, help_text="Average expected delivery lead time in days")
    minimum_order_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Minimum order value in INR")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.50, help_text="Rating out of 5.0")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    categories = models.ManyToManyField(ProductCategory, blank=True, related_name='suppliers')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'suppliers'
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.city})"

    @property
    def is_active(self):
        return self.status == 'active'

class SupplierContact(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='additional_contacts')
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'supplier_contacts'
        verbose_name = 'Supplier Contact'
        verbose_name_plural = 'Supplier Contacts'

    def __str__(self):
        return f"{self.name} - {self.supplier.name}"
