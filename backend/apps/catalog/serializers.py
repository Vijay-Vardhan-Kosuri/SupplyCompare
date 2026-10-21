from rest_framework import serializers
from apps.catalog.models import ProductCategory, Product, UnitConversion

class ProductCategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'description', 'icon_name', 'is_active', 'product_count', 'created_at']

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()

class UnitConversionSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = UnitConversion
        fields = ['id', 'product', 'product_name', 'from_unit', 'to_unit', 'conversion_factor', 'notes']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    standard_unit_display = serializers.CharField(source='get_standard_unit_display', read_only=True)
    active_quotations_count = serializers.SerializerMethodField()
    lowest_active_price = serializers.SerializerMethodField()
    conversions = UnitConversionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'category', 'category_name', 'brand',
            'standard_unit', 'standard_unit_display', 'description',
            'min_stock_alert', 'target_purchase_price', 'is_active',
            'active_quotations_count', 'lowest_active_price', 'conversions',
            'created_at', 'updated_at'
        ]

    def get_active_quotations_count(self, obj):
        # We query the quotations related name
        if hasattr(obj, 'quotations'):
            return obj.quotations.filter(status='active').count()
        return 0

    def get_lowest_active_price(self, obj):
        if hasattr(obj, 'quotations'):
            lowest = obj.quotations.filter(status='active').order_by('unit_price').first()
            if lowest:
                return float(lowest.unit_price)
        return None
