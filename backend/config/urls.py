from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_health(request):
    return JsonResponse({
        'status': 'healthy',
        'platform': 'SupplyCompare API',
        'version': '1.0.0',
        'database': 'MySQL'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/health/', api_health, name='api_health'),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/catalog/', include('apps.catalog.urls')),
    path('api/v1/suppliers/', include('apps.suppliers.urls')),
    path('api/v1/quotations/', include('apps.quotations.urls')),
    path('api/v1/comparison/', include('apps.comparison.urls')),
    path('api/v1/purchasing/', include('apps.purchasing.urls')),
    path('api/v1/inventory/', include('apps.inventory.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
]
