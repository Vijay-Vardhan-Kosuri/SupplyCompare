import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from rest_framework import authentication, exceptions
from apps.accounts.models import User

def generate_tokens_for_user(user):
    """Generate access and refresh tokens for authenticated user."""
    access_payload = {
        'user_id': user.id,
        'email': user.email,
        'role': user.role,
        'exp': datetime.now(timezone.utc) + timedelta(hours=getattr(settings, 'JWT_ACCESS_EXPIRATION_HOURS', 24)),
        'iat': datetime.now(timezone.utc),
        'type': 'access'
    }

    refresh_payload = {
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(days=7),
        'iat': datetime.now(timezone.utc),
        'type': 'refresh'
    }

    secret = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
    algorithm = getattr(settings, 'JWT_ALGORITHM', 'HS256')

    access_token = jwt.encode(access_payload, secret, algorithm=algorithm)
    refresh_token = jwt.encode(refresh_payload, secret, algorithm=algorithm)

    return {
        'access': access_token,
        'refresh': refresh_token
    }

class JWTAuthentication(authentication.BaseAuthentication):
    """Custom JWT Authentication class for Django REST Framework."""

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None

        token = parts[1]
        secret = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
        algorithm = getattr(settings, 'JWT_ALGORITHM', 'HS256')

        try:
            payload = jwt.decode(token, secret, algorithms=[algorithm])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Authentication token has expired.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid authentication token.')

        user_id = payload.get('user_id')
        if not user_id:
            raise exceptions.AuthenticationFailed('User identifier missing in token.')

        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User account no longer exists or is inactive.')

        return (user, token)
