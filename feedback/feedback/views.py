from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from .forms import (
    StudentLoginForm,
    FeedbackForm,
    ChangePasswordForm,
    ForgotPasswordForm,
    StudentRegistrationForm,
)
from .models import Student, Feedback


# 🔹 Student Registration
def student_register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect("login")
    else:
        form = StudentRegistrationForm()

    return render(request, "register.html", {"form": form})


# 🔹 Student Login
def student_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        rollno = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=rollno, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid Roll Number or Password")

    form = StudentLoginForm()
    return render(request, "login.html", {"form": form})


# 🔹 Dashboard
@login_required
def dashboard(request):
    return render(request, "dashboard.html")


# 🔹 Feedback
@login_required
def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            Feedback.objects.create(
                student=request.user,
                course=request.POST.get("course"),
                lecturer=request.POST.get("lecturer"),
                feedback_text=form.cleaned_data["feedback_text"],
                rating=form.cleaned_data["rating"],
            )
            messages.success(request, "Feedback submitted successfully!")
            return redirect("thankyou")
    else:
        form = FeedbackForm()

    return render(request, "feedback.html", {"form": form})


# 🔹 Thank You
def thankyou(request):
    return render(request, "thankyou.html")


# 🔹 Forgot Password
def forgot_password(request):
    form = ForgotPasswordForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            messages.error(request, "No account found with this Email")
            return redirect("forgot_password")

        # ✅ Generate token + uid
        token = default_token_generator.make_token(student)
        uid = urlsafe_base64_encode(force_bytes(student.pk))

        # ✅ Current site domain
        domain = get_current_site(request).domain

        subject = "Password Reset Request"
        html_message = render_to_string("reset_email.html", {
            "user": student,
            "uid": uid,
            "token": token,
            "domain": domain,
        })

        email_message = EmailMultiAlternatives(
            subject, "", settings.DEFAULT_FROM_EMAIL, [email]
        )
        email_message.attach_alternative(html_message, "text/html")
        email_message.send()

        messages.success(request, f"Password reset link sent to {email}")
        return redirect("reset_success")

    return render(request, "forgot_password.html", {"form": form})


# 🔹 Reset Password (from email link)
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        student = Student.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Student.DoesNotExist):
        student = None

    if student is not None and default_token_generator.check_token(student, token):
        if request.method == "POST":
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match")
            else:
                student.set_password(new_password)
                student.save()
                messages.success(request, "Password reset successful. Please login.")
                return redirect("login")

        return render(request, "reset_form.html", {"validlink": True})
    else:
        return render(request, "reset_form.html", {"validlink": False})


# 🔹 Reset Success
def reset_success(request):
    return render(request, "reset_success.html")


# 🔹 Change Password
@login_required
def change_password(request):
    form = ChangePasswordForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        old = form.cleaned_data["old_password"]
        new = form.cleaned_data["new_password"]
        confirm = form.cleaned_data["confirm_password"]

        if new != confirm:
            messages.error(request, "Passwords do not match")
        elif not request.user.check_password(old):
            messages.error(request, "Old password incorrect")
        else:
            request.user.set_password(new)
            request.user.save()
            messages.success(request, "Password updated successfully. Please login again.")
            logout(request)  # logout after password change
            return redirect("login")

    return render(request, "change_password.html", {"form": form})


# 🔹 Change Success (optional page)
def change_success(request):
    return render(request, "change_success.html")


# 🔹 Logout
def logout_view(request):
    logout(request)
    return redirect("login")
