from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Feedback


# 🔹 Custom Student Admin
class StudentAdmin(UserAdmin):
    model = Student
    list_display = ("rollno", "name", "branch", "year", "course", "is_active", "is_staff")
    search_fields = ("rollno", "name", "branch", "year", "course")
    ordering = ("rollno",)

    fieldsets = (
        (None, {"fields": ("rollno", "name", "branch", "year", "course", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("rollno", "name", "branch", "year", "course", "password1", "password2", "is_active", "is_staff")}
        ),
    )


# 🔹 Feedback Admin
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("student", "rating", "submitted_at")
    search_fields = ("student__rollno", "student__name", "rating")
    list_filter = ("rating", "submitted_at")


# ✅ Register models in admin
admin.site.register(Student, StudentAdmin)
admin.site.register(Feedback, FeedbackAdmin)
