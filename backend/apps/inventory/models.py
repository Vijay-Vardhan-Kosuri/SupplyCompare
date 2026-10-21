from django.db import models
from django.utils import timezone
from apps.accounts.models import User
from apps.catalog.models import Product

class StockItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_items', help_text="Retailer owning this stock")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_records')
    current_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    low_stock_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    last_restocked_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory_stock_items'
        verbose_name = 'Stock Item'
        verbose_name_plural = 'Stock Items'
        unique_together = ('user', 'product')
        ordering = ['product__name']

    def __str__(self):
        return f"{self.product.name}: {self.current_stock} {self.product.standard_unit}"

    @property
    def is_low_stock(self):
        return self.current_stock <= self.low_stock_threshold


class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = (
        ('purchase_receipt', 'Purchase Order Receipt'),
        ('adjustment_add', 'Inventory Adjustment (+ Stock)'),
        ('adjustment_subtract', 'Inventory Adjustment (- Stock)'),
        ('damaged', 'Damaged / Spoiled Goods'),
        ('sale', 'Customer Sale'),
        ('supplier_return', 'Return to Supplier'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_movements')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=30, choices=MOVEMENT_TYPE_CHOICES, db_index=True)
    quantity_delta = models.DecimalField(max_digits=10, decimal_places=2, help_text="Positive for addition, negative for deduction")
    unit = models.CharField(max_length=30)
    previous_stock = models.DecimalField(max_digits=12, decimal_places=2)
    resulting_stock = models.DecimalField(max_digits=12, decimal_places=2)
    reference_id = models.CharField(max_length=100, blank=True, help_text="PO number or transaction reference")
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'inventory_stock_movements'
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')}: {self.product.name} {self.quantity_delta:+g} ({self.get_movement_type_display()})"
