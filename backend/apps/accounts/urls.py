from django.urls import path
from apps.accounts.views import (
    RegisterView, LoginView, CurrentUserView,
    PasswordResetRequestView, AdminUserListView, AdminToggleUserStatusView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('me/', CurrentUserView.as_view(), name='auth_me'),
    path('forgot-password/', PasswordResetRequestView.as_view(), name='auth_forgot_password'),
    path('users/', AdminUserListView.as_view(), name='admin_users_list'),
    path('users/<int:user_id>/toggle-status/', AdminToggleUserStatusView.as_view(), name='admin_user_toggle'),
]
