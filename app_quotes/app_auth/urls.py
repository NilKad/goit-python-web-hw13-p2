from . import views
from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .forms import LoginForm

app_name = "app_auth"

urlpatterns = [
    path("signup/", views.RegisetrView.as_view(), name="signup"),
    path(
        "signin/",
        LoginView.as_view(
            template_name="app_auth/login.html",
            form_class=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="signin",
    ),
    path(
        "logout/",
        views.CustomLogoutView.as_view(template_name="app_auth/logout.html"),
        name="logout",
    ),
    # path("profile/", views.profile, name="profile"),
    path(
        "reset-password/",
        views.ResetPasswordView.as_view(),
        name="password_reset",
    ),
    path(
        "reset-password/done/",
        PasswordResetDoneView.as_view(
            template_name="app_auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="app_auth/password_reset_confirm.html",
            success_url="/auth/reset-password/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        PasswordResetCompleteView.as_view(
            template_name="app_auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
