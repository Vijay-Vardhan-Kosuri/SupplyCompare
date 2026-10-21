from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from django.db.models import Q, Avg, Count
from apps.suppliers.models import Supplier, SupplierContact
from apps.suppliers.serializers import SupplierSerializer, SupplierContactSerializer
from apps.accounts.permissions import IsRetailerOrSupplier

class SupplierListCreateView(generics.ListCreateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Supplier.objects.all().prefetch_related('categories', 'additional_contacts')
        q = self.request.query_params.get('q')
        status_param = self.request.query_params.get('status')
        city = self.request.query_params.get('city')
        category_id = self.request.query_params.get('category')

        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(contact_person__icontains=q) |
                Q(phone__icontains=q) |
                Q(gstin__icontains=q)
            )
        if status_param:
            qs = qs.filter(status=status_param)
        else:
            # Default to active unless explicitly asking for archived/all
            if not self.request.query_params.get('all'):
                qs = qs.exclude(status='archived')

        if city:
            qs = qs.filter(city__iexact=city)
        if category_id:
            qs = qs.filter(categories__id=category_id)

        return qs.order_by('name')

class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all().prefetch_related('categories', 'additional_contacts')
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # Soft-delete by setting status to archived
        instance.status = 'archived'
        instance.save()

class SupplierContactCreateView(generics.CreateAPIView):
    queryset = SupplierContact.objects.all()
    serializer_class = SupplierContactSerializer
    permission_classes = [permissions.IsAuthenticated]

class SupplierStatsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total_suppliers = Supplier.objects.exclude(status='archived').count()
        active_suppliers = Supplier.objects.filter(status='active').count()
        avg_rating = Supplier.objects.filter(status='active').aggregate(Avg('rating'))['rating__avg'] or 0.0
        avg_lead_days = Supplier.objects.filter(status='active').aggregate(Avg('delivery_lead_days'))['delivery_lead_days__avg'] or 0.0

        return Response({
            'total_suppliers': total_suppliers,
            'active_suppliers': active_suppliers,
            'average_rating': round(float(avg_rating), 1),
            'average_lead_days': round(float(avg_lead_days), 1),
        })
