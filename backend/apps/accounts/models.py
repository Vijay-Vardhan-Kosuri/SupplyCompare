from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('retailer', 'Retailer'),
        ('supplier', 'Supplier'),
        ('admin', 'Platform Administrator'),
    )

    email = models.EmailField(unique=True, max_length=255, db_index=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='retailer', db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def full_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.email

    @property
    def is_retailer(self):
        return self.role == 'retailer'

    @property
    def is_supplier(self):
        return self.role == 'supplier'

    @property
    def is_platform_admin(self):
        return self.role == 'admin' or self.is_superuser


class RetailerProfile(models.Model):
    SHOP_TYPE_CHOICES = (
        ('kirana', 'Kirana / Grocery Store'),
        ('supermarket', 'Supermarket / Minimart'),
        ('convenience', 'Convenience Store'),
        ('fmcg', 'FMCG Retail'),
        ('pharmacy', 'Pharmacy & Health'),
        ('general', 'General Merchant'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='retailer_profile')
    shop_name = models.CharField(max_length=200)
    gstin = models.CharField(max_length=30, blank=True, help_text="Goods & Services Tax Identification Number")
    shop_type = models.CharField(max_length=30, choices=SHOP_TYPE_CHOICES, default='kirana')
    address_line = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, default='Hyderabad')
    state = models.CharField(max_length=100, default='Telangana')
    pincode = models.CharField(max_length=20, blank=True)
    currency = models.CharField(max_length=10, default='INR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'retailer_profiles'
        verbose_name = 'Retailer Profile'
        verbose_name_plural = 'Retailer Profiles'

    def __str__(self):
        return f"{self.shop_name} ({self.user.email})"


class SupplierProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supplier_profile')
    # Link to a Supplier directory entity (nullable because manual entry exists)
    supplier_id = models.IntegerField(null=True, blank=True, help_text="Foreign ID to suppliers.Supplier record")
    business_name = models.CharField(max_length=200)
    designation = models.CharField(max_length=100, blank=True, default='Sales Manager')
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'supplier_profiles'
        verbose_name = 'Supplier Profile'
        verbose_name_plural = 'Supplier Profiles'

    def __str__(self):
        return f"{self.business_name} - {self.user.email}"
