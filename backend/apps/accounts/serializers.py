from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.accounts.models import User, RetailerProfile, SupplierProfile

class RetailerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerProfile
        fields = [
            'id', 'shop_name', 'gstin', 'shop_type',
            'address_line', 'city', 'state', 'pincode', 'currency'
        ]

class SupplierProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierProfile
        fields = ['id', 'supplier_id', 'business_name', 'designation', 'is_verified']

class UserSerializer(serializers.ModelSerializer):
    retailer_profile = RetailerProfileSerializer(read_only=True)
    supplier_profile = SupplierProfileSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone',
            'role', 'full_name', 'is_active', 'date_joined',
            'retailer_profile', 'supplier_profile'
        ]
        read_only_fields = ['id', 'role', 'date_joined']

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=['retailer', 'supplier'], default='retailer')

    # Profile fields
    shop_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    shop_type = serializers.CharField(max_length=30, required=False, default='kirana')
    city = serializers.CharField(max_length=100, required=False, allow_blank=True, default='Hyderabad')
    business_name = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email address already exists.')
        return value.lower()

    def create(self, validated_data):
        role = validated_data.get('role', 'retailer')
        shop_name = validated_data.pop('shop_name', None)
        shop_type = validated_data.pop('shop_type', 'kirana')
        city = validated_data.pop('city', 'Hyderabad')
        business_name = validated_data.pop('business_name', None)

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            role=role
        )

        if role == 'retailer':
            name = shop_name or f"{user.first_name}'s Store" if user.first_name else "Retail Store"
            RetailerProfile.objects.create(
                user=user,
                shop_name=name,
                shop_type=shop_type,
                city=city or 'Hyderabad'
            )
        elif role == 'supplier':
            b_name = business_name or f"{user.first_name}'s Supplies" if user.first_name else "Supplier Enterprise"
            SupplierProfile.objects.create(
                user=user,
                business_name=b_name
            )

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '').lower()
        password = attrs.get('password')

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password.')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password.')

        if not user.is_active:
            raise serializers.ValidationError('This user account has been disabled.')

        attrs['user'] = user
        return attrs

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('No account found with this email address.')
        return value.lower()
