"""
URL configuration for authentication endpoints.
Includes registration, login, and email check routes.
"""
from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.RegistrationView.as_view(), name='register'),
  path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
  path('login/', views.LoginView.as_view(), name='login'),
  path('logout/', views.LogoutView.as_view(), name='logout'),
  path('password_reset/', views.PasswordResetView.as_view(), name='password-reset'),
  path('password_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
  path('token/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
]