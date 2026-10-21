from rest_framework import generics, permissions, filters, views, status
from rest_framework.response import Response
from django.db.models import Q
from apps.catalog.models import ProductCategory, Product, UnitConversion
from apps.catalog.serializers import (
    ProductCategorySerializer, ProductSerializer, UnitConversionSerializer
)
from apps.accounts.permissions import IsRetailerOrSupplier, IsPlatformAdmin

class ProductCategoryListCreateView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all().order_by('name')
    serializer_class = ProductCategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsRetailerOrSupplier()]
        return [permissions.IsAuthenticated()]

class ProductCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsRetailerOrSupplier]

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsRetailerOrSupplier()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = Product.objects.all().select_related('category').prefetch_related('conversions')
        q = self.request.query_params.get('q')
        category = self.request.query_params.get('category')
        brand = self.request.query_params.get('brand')
        is_active = self.request.query_params.get('is_active')

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(sku__icontains=q) | Q(brand__icontains=q))
        if category:
            qs = qs.filter(Q(category__slug=category) | Q(category__id=category) if category.isdigit() else Q(category__slug=category))
        if brand:
            qs = qs.filter(brand__iexact=brand)
        if is_active is not None:
            qs = qs.filter(is_active=(is_active.lower() == 'true'))

        return qs.order_by('name')

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().select_related('category').prefetch_related('conversions')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsRetailerOrSupplier]

class UnitConversionListCreateView(generics.ListCreateAPIView):
    queryset = UnitConversion.objects.all().select_related('product')
    serializer_class = UnitConversionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        product_id = self.request.query_params.get('product_id')
        if product_id:
            qs = qs.filter(Q(product_id=product_id) | Q(product__isnull=True))
        return qs

class CatalogMetaView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = ProductCategory.objects.filter(is_active=True).values('id', 'name', 'slug')
        brands = Product.objects.filter(is_active=True).values_list('brand', flat=True).distinct()
        brands = sorted([b for b in brands if b])
        unit_choices = [{'value': u[0], 'label': u[1]} for u in Product.UNIT_CHOICES]

        return Response({
            'categories': categories,
            'brands': brands,
            'unit_choices': unit_choices,
            'total_products': Product.objects.filter(is_active=True).count()
        })
