from django.urls import path
from apps.catalog.views import (
    ProductCategoryListCreateView, ProductCategoryDetailView,
    ProductListCreateView, ProductDetailView,
    UnitConversionListCreateView, CatalogMetaView
)

urlpatterns = [
    path('categories/', ProductCategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<int:pk>/', ProductCategoryDetailView.as_view(), name='category_detail'),
    path('products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('conversions/', UnitConversionListCreateView.as_view(), name='conversion_list_create'),
    path('meta/', CatalogMetaView.as_view(), name='catalog_meta'),
]
