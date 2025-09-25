from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Student


# 🔹 Registration Form
class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")

    class Meta:
        model = Student
        fields = [
            "rollno",    # student unique ID
            "name",      # student name
            "branch",    # branch (CSE, ECE, etc.)
            "year",      # year of study
            "course",    # course (B.Tech, M.Tech, etc.)
            "email",     # email (required for password reset)
            "password1", # password
            "password2", # confirm password
        ]


# 🔹 Login Form
class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(label="Roll Number")
    password = forms.CharField(widget=forms.PasswordInput)


# 🔹 Feedback Form
class FeedbackForm(forms.Form):
    CHOICES = [
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("average", "Average"),
        ("poor", "Poor"),
    ]
    feedback_text = forms.CharField(widget=forms.Textarea, label="Your Feedback")
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


# 🔹 Change Password Form
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")


# 🔹 Forgot Password Form
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Registered Email")
