from rest_framework import serializers
from apps.suppliers.models import Supplier, SupplierContact
from apps.catalog.serializers import ProductCategorySerializer

class SupplierContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierContact
        fields = ['id', 'supplier', 'name', 'designation', 'phone', 'email', 'is_primary']

class SupplierSerializer(serializers.ModelSerializer):
    category_details = ProductCategorySerializer(source='categories', many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, required=False, source='categories',
        queryset=Supplier.categories.rel.model.objects.all()
    )
    additional_contacts = SupplierContactSerializer(many=True, read_only=True)
    payment_terms_display = serializers.CharField(source='get_payment_terms_display', read_only=True)
    active_quotations_count = serializers.SerializerMethodField()
    completed_orders_count = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'gstin', 'contact_person', 'phone', 'email',
            'address', 'city', 'state', 'pincode', 'payment_terms',
            'payment_terms_display', 'delivery_lead_days', 'minimum_order_value',
            'rating', 'status', 'category_details', 'category_ids',
            'additional_contacts', 'notes', 'active_quotations_count',
            'completed_orders_count', 'created_at', 'updated_at'
        ]

    def get_active_quotations_count(self, obj):
        if hasattr(obj, 'quotations'):
            return obj.quotations.filter(status='active').count()
        return 0

    def get_completed_orders_count(self, obj):
        if hasattr(obj, 'purchase_orders'):
            return obj.purchase_orders.filter(status='received').count()
        return 0
