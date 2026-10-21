from rest_framework.permissions import BasePermission

class IsRetailer(BasePermission):
    """Allows access only to authenticated retailers or superusers."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'retailer' or request.user.is_superuser)
        )

class IsSupplier(BasePermission):
    """Allows access only to authenticated suppliers or superusers."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'supplier' or request.user.is_superuser)
        )

class IsPlatformAdmin(BasePermission):
    """Allows access only to platform administrators or superusers."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.is_superuser)
        )

class IsRetailerOrSupplier(BasePermission):
    """Allows access to both retailers and suppliers."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role in ['retailer', 'supplier', 'admin'] or request.user.is_superuser)
        )
