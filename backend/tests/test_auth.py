from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User, RetailerProfile, SupplierProfile

class AuthenticationAndRBACTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create admin user
        self.admin = User.objects.create_superuser(
            email='admin_test@supplycompare.local',
            password='AdminTestPassword123'
        )

        # Create retailer user
        self.retailer = User.objects.create_user(
            email='retailer_test@supplycompare.local',
            password='RetailerTestPassword123',
            role='retailer'
        )
        RetailerProfile.objects.create(
            user=self.retailer,
            shop_name='Test Kirana Store',
            city='Hyderabad'
        )

        # Create supplier user
        self.supplier = User.objects.create_user(
            email='supplier_test@supplycompare.local',
            password='SupplierTestPassword123',
            role='supplier'
        )
        SupplierProfile.objects.create(
            user=self.supplier,
            business_name='Test Supplier Wholesaler'
        )

    def test_register_retailer_success(self):
        payload = {
            'email': 'new_retailer@supplycompare.local',
            'password': 'SecurePassword123',
            'first_name': 'Anil',
            'last_name': 'Kumar',
            'role': 'retailer',
            'shop_name': 'Anil Provision Stores',
            'city': 'Bengaluru'
        }
        response = self.client.post('/api/v1/auth/register/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertEqual(response.data['user']['email'], 'new_retailer@supplycompare.local')
        self.assertEqual(response.data['user']['role'], 'retailer')

        # Check DB
        user = User.objects.get(email='new_retailer@supplycompare.local')
        self.assertTrue(hasattr(user, 'retailer_profile'))
        self.assertEqual(user.retailer_profile.shop_name, 'Anil Provision Stores')

    def test_login_success_and_jwt_issuance(self):
        payload = {
            'email': 'retailer_test@supplycompare.local',
            'password': 'RetailerTestPassword123'
        }
        response = self.client.post('/api/v1/auth/login/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        token = response.data['tokens']['access']

        # Access authenticated me endpoint with JWT Bearer
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        me_resp = self.client.get('/api/v1/auth/me/')
        self.assertEqual(me_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(me_resp.data['user']['email'], 'retailer_test@supplycompare.local')

    def test_login_invalid_password(self):
        payload = {
            'email': 'retailer_test@supplycompare.local',
            'password': 'WrongPasswordXYZ'
        }
        response = self.client.post('/api/v1/auth/login/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_user_list_permission_enforcement(self):
        # Non-admin retailer should be denied access to admin users list
        login_resp = self.client.post('/api/v1/auth/login/', {
            'email': 'retailer_test@supplycompare.local',
            'password': 'RetailerTestPassword123'
        })
        token = login_resp.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        resp = self.client.get('/api/v1/auth/users/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Admin should have full access
        admin_login = self.client.post('/api/v1/auth/login/', {
            'email': 'admin_test@supplycompare.local',
            'password': 'AdminTestPassword123'
        })
        admin_token = admin_login.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        admin_resp = self.client.get('/api/v1/auth/users/')
        self.assertEqual(admin_resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(admin_resp.data), 3)
