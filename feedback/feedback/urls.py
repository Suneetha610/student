from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Registration & Auth
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
    path("reset/<uidb64>/<token>/", views.reset_password, name="reset_password"),  # 👈 custom reset view
    path("change-password/", views.change_password, name="change_password"),
    path("change-success/", views.change_success, name="change_success"),
]
