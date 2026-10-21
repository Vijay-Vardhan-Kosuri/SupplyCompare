from django.db import models
from django.utils.text import slugify

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, blank=True, default='Package', help_text="Lucide icon name")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'catalog_categories'
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    UNIT_CHOICES = (
        ('piece', 'Piece / Unit'),
        ('kg', 'Kilogram (kg)'),
        ('g', 'Gram (g)'),
        ('quintal', 'Quintal (100 kg)'),
        ('litre', 'Litre (L)'),
        ('ml', 'Millilitre (ml)'),
        ('carton', 'Carton'),
        ('box', 'Box'),
        ('packet', 'Packet'),
        ('bag', 'Bag'),
        ('tin', 'Tin / Can'),
        ('dozen', 'Dozen (12 pcs)'),
    )

    name = models.CharField(max_length=200, db_index=True)
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    brand = models.CharField(max_length=100, blank=True, db_index=True)
    standard_unit = models.CharField(max_length=30, choices=UNIT_CHOICES, default='piece')
    description = models.TextField(blank=True)
    min_stock_alert = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    target_purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Benchmark target price in INR")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog_products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sku})"

class UnitConversion(models.Model):
    """
    Conversion factor to convert from_unit to to_unit.
    Rule: 1 from_unit = conversion_factor * to_unit.
    Example: 1 carton of biscuits = 24 packets => from_unit='carton', to_unit='packet', factor=24
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='conversions')
    from_unit = models.CharField(max_length=30)
    to_unit = models.CharField(max_length=30)
    conversion_factor = models.DecimalField(max_digits=12, decimal_places=4)
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'catalog_unit_conversions'
        verbose_name = 'Unit Conversion'
        verbose_name_plural = 'Unit Conversions'
        unique_together = ('product', 'from_unit', 'to_unit')

    def __str__(self):
        prod = self.product.name if self.product else "Global"
        return f"[{prod}] 1 {self.from_unit} = {self.conversion_factor} {self.to_unit}"
