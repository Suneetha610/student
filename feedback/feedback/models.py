from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# 🔹 Custom Manager for Student
class StudentManager(BaseUserManager):
    def create_user(self, rollno, email, password=None, **extra_fields):
        if not rollno:
            raise ValueError("The Roll Number field is required")
        if not email:
            raise ValueError("The Email field is required")

        email = self.normalize_email(email)
        student = self.model(rollno=rollno, email=email, **extra_fields)
        student.set_password(password)
        student.save(using=self._db)
        return student

    def create_superuser(self, rollno, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(rollno, email, password, **extra_fields)


# 🔹 Custom Student User Model
class Student(AbstractBaseUser, PermissionsMixin):
    rollno = models.CharField(max_length=20, unique=True, verbose_name="Roll Number")
    name = models.CharField(max_length=100, verbose_name="Full Name")
    branch = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)

    # 🔹 Email field (nullable only for old rows – new users must give email)
    email = models.EmailField(unique=True, verbose_name="Email Address", null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # required for Django admin

    USERNAME_FIELD = "rollno"               # 🔑 Roll No will be used for login
    REQUIRED_FIELDS = ["name", "email"]     # required when creating superuser

    objects = StudentManager()

    def __str__(self):
        return f"{self.rollno} - {self.name}"


# 🔹 Feedback Model (to store feedback in DB)
class Feedback(models.Model):
    RATING_CHOICES = [
        ("poor", "Poor"),
        ("average", "Average"),
        ("good", "Good"),
        ("excellent", "Excellent"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lecturer = models.CharField(max_length=100, blank=True, null=True)
    feedback_text = models.TextField()
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.rollno} - {self.rating}"
