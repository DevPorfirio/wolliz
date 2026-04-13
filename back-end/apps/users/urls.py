from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    path("register", views.RegisterView.as_view(), name="auth-register"),
    path("token", TokenObtainPairView.as_view(), name="auth-token"),
    path("token/refresh", TokenRefreshView.as_view(), name="auth-token-refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="auth-token-verify"),
    path("logout", views.LogoutView.as_view(), name="auth-logout"),
    path("me", views.MeView.as_view(), name="auth-me"),
    path("profile", views.ProfileUpdateView.as_view(), name="auth-profile"),
    path("change-password", views.ChangePasswordView.as_view(), name="auth-change-password"),
    path("forgot-password", views.ForgotPasswordView.as_view(), name="auth-forgot-password"),
    path("avatar", views.AvatarUpdateView.as_view(), name="auth-avatar"),
]
