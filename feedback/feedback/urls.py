from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # 🔹 First Registration
    path("", views.student_register, name="register"),
    path("login/", views.student_login, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # 🔹 Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # 🔹 Feedback
    path("feedback/", views.feedback, name="feedback"),
    path("thankyou/", views.thankyou, name="thankyou"),

    # 🔹 Password management (custom)
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-success/", views.reset_success, name="reset_success"),
    path("change-password/", views.change_password, name="change_password"),
    path("change-success/", views.change_success, name="change_success"),

    # 🔹 Built-in reset flow (with your template names)
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="reset_form.html"   # 👈 user sets new password here
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="reset_success.html"  # 👈 success page
        ),
        name="password_reset_complete",
    ),
]
