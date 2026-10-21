from django.urls import path
from apps.suppliers.views import (
    SupplierListCreateView, SupplierDetailView,
    SupplierContactCreateView, SupplierStatsView
)

urlpatterns = [
    path('', SupplierListCreateView.as_view(), name='supplier_list_create'),
    path('<int:pk>/', SupplierDetailView.as_view(), name='supplier_detail'),
    path('contacts/', SupplierContactCreateView.as_view(), name='supplier_contact_create'),
    path('stats/', SupplierStatsView.as_view(), name='supplier_stats'),
]
