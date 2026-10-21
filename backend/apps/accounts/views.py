from rest_framework import status, views, permissions
from rest_framework.response import Response
from apps.accounts.serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    RetailerProfileSerializer, SupplierProfileSerializer,
    PasswordResetRequestSerializer
)
from apps.accounts.authentication import generate_tokens_for_user
from apps.accounts.permissions import IsPlatformAdmin
from apps.accounts.models import User, RetailerProfile, SupplierProfile

class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = generate_tokens_for_user(user)

        user_data = UserSerializer(user).data
        return Response({
            'message': 'Account registered successfully',
            'user': user_data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = generate_tokens_for_user(user)

        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': tokens
        }, status=status.HTTP_200_OK)

class CurrentUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'user': UserSerializer(request.user).data
        })

    def patch(self, request):
        user = request.user
        data = request.data

        # Update base user fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        user.save()

        # Update profile if applicable
        if user.is_retailer and hasattr(user, 'retailer_profile'):
            profile = user.retailer_profile
            p_data = data.get('retailer_profile', {})
            for field in ['shop_name', 'gstin', 'shop_type', 'address_line', 'city', 'state', 'pincode', 'currency']:
                if field in p_data:
                    setattr(profile, field, p_data[field])
            profile.save()
        elif user.is_supplier and hasattr(user, 'supplier_profile'):
            profile = user.supplier_profile
            p_data = data.get('supplier_profile', {})
            if 'business_name' in p_data:
                profile.business_name = p_data['business_name']
            if 'designation' in p_data:
                profile.designation = p_data['designation']
            profile.save()

        return Response({
            'message': 'Profile updated successfully',
            'user': UserSerializer(user).data
        })

class PasswordResetRequestView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        # In a real environment, send reset email with token
        return Response({
            'message': f'Password reset link generated for {email}. Please check your inbox.',
            'reset_token_simulated': 'reset-token-valid-for-15-mins'
        }, status=status.HTTP_200_OK)

class AdminUserListView(views.APIView):
    permission_classes = [IsPlatformAdmin]

    def get(self, request):
        users = User.objects.all().order_by('-date_joined')
        role_filter = request.query_params.get('role')
        if role_filter:
            users = users.filter(role=role_filter)
        return Response(UserSerializer(users, many=True).data)

class AdminToggleUserStatusView(views.APIView):
    permission_classes = [IsPlatformAdmin]

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if target_user.is_superuser:
            return Response({'error': 'Cannot disable superuser'}, status=status.HTTP_400_BAD_REQUEST)

        target_user.is_active = not target_user.is_active
        target_user.save()

        return Response({
            'message': f"User account {'activated' if target_user.is_active else 'deactivated'} successfully",
            'user': UserSerializer(target_user).data
        })
