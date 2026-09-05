from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Destination, TourPackage
from django.core.mail import send_mail
from .models import Review
from .forms import ReviewForm


# =====================================================
# HOME
# =====================================================

def home(request):

    destinations = Destination.objects.filter(
        is_available=True
    ).order_by("-created_at")

    return render(
        request,
        "home.html",
        {
            "destinations": destinations
        }
    )


# =====================================================
# REGISTER
# =====================================================

def register(request):
  

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")


    return render(request, "register.html")
    return redirect("registration_success")

def registration_success(request):
    return render(request, "registration_success.html")    


# =====================================================
# LOGIN
# =====================================================

def user_login(request):

    if request.user.is_authenticated:
        messages.info(
            request,
            "You are already logged in."
        )
        return redirect("home")

    if request.method == "POST":

        login_input = request.POST.get(
            "login_input",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        if not login_input or not password:

            messages.error(
                request,
                "Please enter your username/email and password."
            )

            return render(request, "login.html")

        user = None

        # Email login
        if "@" in login_input:

            try:

                user_obj = User.objects.get(
                    email__iexact=login_input
                )

                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )

            except User.DoesNotExist:

                messages.error(
                    request,
                    "No account found with this email address."
                )

                return render(request, "login.html")

        # Username login
        else:

            try:

                user_obj = User.objects.get(
                    username__iexact=login_input
                )

            except User.DoesNotExist:

                messages.error(
                    request,
                    "Username not found. Please register first."
                )

                return render(request, "login.html")

            # Use actual username so case-insensitive login works
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

        # Wrong password
        if user is None:

            messages.error(
                request,
                "Incorrect password. Please try again."
            )

            return render(request, "login.html")

        # Login
        login(request, user)

        messages.success(
            request,
            f"Welcome back, {user.username}! "
        )

        next_url = request.GET.get("next")

        if next_url:
            return redirect(next_url)

        return redirect("home")

    return render(
        request,
        "login.html"
    )


# =====================================================
# LOGOUT CONFIRMATION
# =====================================================

@login_required(login_url="login")
def user_logout(request):

    if request.method == "POST":

        logout(request)

        messages.success(
            request,
            "You have been logged out successfully."
        )

        return redirect("home")

    return render(
        request,
        "logout_confirm.html"
    )


# =====================================================
# FORGOT PASSWORD
# =====================================================

class CustomPasswordResetView(PasswordResetView):

    template_name = "forgot_password.html"

    email_template_name = "password_reset_email.html"

    subject_template_name = "password_reset_subject.txt"

    success_url = reverse_lazy(
        "password_reset_done"
    )


# =====================================================
# PROFILE
# =====================================================

@login_required(login_url="login")
def profile(request):

    user = request.user

    return render(
        request,
        "profile.html",
        {
            "profile_user": user
        }
    )


# =====================================================
# EDIT PROFILE
# =====================================================

@login_required(login_url="login")
def edit_profile(request):

    user = request.user

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        # -----------------------------
        # REQUIRED FIELDS
        # -----------------------------

        if not username or not email:

            messages.error(
                request,
                "Username and email are required."
            )

            return render(
                request,
                "edit_profile.html"
            )

        # -----------------------------
        # USERNAME VALIDATION
        # -----------------------------

        if len(username) < 3:

            messages.error(
                request,
                "Username must contain at least 3 characters."
            )

            return render(
                request,
                "edit_profile.html"
            )

        if not username.replace("_", "").isalnum():

            messages.error(
                request,
                "Username can contain only letters, numbers and underscore."
            )

            return render(
                request,
                "edit_profile.html"
            )

        # Check duplicate username
        if User.objects.filter(
            username__iexact=username
        ).exclude(
            pk=user.pk
        ).exists():

            messages.error(
                request,
                "This username is already taken."
            )

            return render(
                request,
                "edit_profile.html"
            )

        # -----------------------------
        # EMAIL VALIDATION
        # -----------------------------

        try:

            validate_email(email)

        except ValidationError:

            messages.error(
                request,
                "Please enter a valid email address."
            )

            return render(
                request,
                "edit_profile.html"
            )

        # Check duplicate email
        if User.objects.filter(
            email__iexact=email
        ).exclude(
            pk=user.pk
        ).exists():

            messages.error(
                request,
                "This email is already registered by another user."
            )

            return render(
                request,
                "edit_profile.html"
            )

        # -----------------------------
        # UPDATE USER
        # -----------------------------

        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        user.save()

        messages.success(
            request,
            "Profile updated successfully! "
        )

        return redirect("profile")

    return render(
        request,
        "edit_profile.html"
    )


# =====================================================
# CHANGE PASSWORD
# =====================================================

@login_required(login_url="login")
def change_password(request):

    if request.method == "POST":

        current_password = request.POST.get(
            "current_password",
            ""
        )

        new_password = request.POST.get(
            "new_password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        # -----------------------------
        # REQUIRED
        # -----------------------------

        if not current_password or not new_password or not confirm_password:

            messages.error(
                request,
                "All password fields are required."
            )

            return render(
                request,
                "change_password.html"
            )

        # -----------------------------
        # CURRENT PASSWORD
        # -----------------------------

        if not request.user.check_password(
            current_password
        ):

            messages.error(
                request,
                "Current password is incorrect."
            )

            return render(
                request,
                "change_password.html"
            )

        # -----------------------------
        # NEW PASSWORD
        # -----------------------------

        if len(new_password) < 8:

            messages.error(
                request,
                "New password must contain at least 8 characters."
            )

            return render(
                request,
                "change_password.html"
            )

        if new_password != confirm_password:

            messages.error(
                request,
                "New passwords do not match."
            )

            return render(
                request,
                "change_password.html"
            )

        if current_password == new_password:

            messages.error(
                request,
                "New password must be different from your current password."
            )

            return render(
                request,
                "change_password.html"
            )

        # -----------------------------
        # SAVE PASSWORD
        # -----------------------------

        request.user.set_password(
            new_password
        )

        request.user.save()

        # Login again after password change
        user = authenticate(
            request,
            username=request.user.username,
            password=new_password
        )

        if user is not None:
            login(request, user)

        messages.success(
            request,
            "Password changed successfully! "
        )

        return redirect("profile")

    return render(
        request,
        "change_password.html"
    )


# =====================================================
# MY BOOKINGS
# =====================================================

@login_required(login_url="login")
def my_bookings(request):

    from booking.models import Booking

    bookings = Booking.objects.filter(
        username__iexact=request.user.username
    ).select_related(
        "package",
        "package__destination"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "my_bookings.html",
        {
            "bookings": bookings
        }
    )


# =====================================================
# DESTINATION LIST
# =====================================================

def destination_list(request):

    destinations = Destination.objects.filter(
        is_available=True
    ).order_by("-created_at")

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:
        destinations = (
            destinations.filter(
                name__icontains=search
            )
            |
            destinations.filter(
                location__icontains=search
            )
        )

    mood = request.GET.get(
        "mood",
        ""
    ).strip()

    if mood:
        destinations = destinations.filter(
            mood=mood
        )

    # ==============================
    # ABOVE BUDGET
    # ==============================

    budget = request.GET.get(
        "budget",
        ""
    ).strip()

    if budget:
        try:
            budget = float(budget)

            destinations = destinations.filter(
                budget__gt=budget
            )

        except (ValueError, TypeError):
            pass

    return render(
        request,
        "destinations/destination_list.html",
        {
            "destinations": destinations,
            "search": search,
            "selected_mood": mood,
            "selected_budget": str(budget),
        }
    )
# =====================================================
# DESTINATION DETAIL
# =====================================================

def destination_detail(request, pk):

    destination = get_object_or_404(
        Destination,
        pk=pk,
        is_available=True
    )

    return render(
        request,
        "destinations/destination_detail.html",
        {
            "destination": destination
        }
    )


# =====================================================
# MOOD PLANNER
# =====================================================

def mood_planner(request):

    mood = request.GET.get(
        "mood",
        ""
    ).strip()

    destinations = Destination.objects.filter(
        is_available=True
    )

    if mood:

        destinations = destinations.filter(
            mood=mood
        )

    return render(
        request,
        "mood_planner.html",
        {
            "destinations": destinations,
            "selected_mood": mood,
        }
    )


# =====================================================
# TOUR PACKAGES
# =====================================================

def tour_packages(request):

    packages = TourPackage.objects.filter(
        is_available=True
    ).select_related(
        "destination"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "tour_packages.html",
        {
            "packages": packages
        }
    )


# =====================================================
# TOUR PACKAGE DETAIL
# =====================================================

def tour_package_detail(request, pk):

    package = get_object_or_404(
        TourPackage,
        pk=pk,
        is_available=True
    )

    return render(
        request,
        "tour_package_detail.html",
        {
            "package": package
        }
    )


# =====================================================
# TRIP WITH STRANGERS
# =====================================================

def strangers_trip(request):

    return render(
        request,
        "strangers_trip.html"
    )


# =====================================================
# SOLO TRIP
# =====================================================

def solo_trip(request):

    return render(
        request,
        "solo_trip.html"
    )


# =====================================================
# KIDS TRIP
# =====================================================

def kids_trip(request):

    return render(
        request,
        "kids_trip.html"
    )

@login_required(login_url="login")
def change_password(request):

    if request.method == "POST":

        current_password = request.POST.get("current_password", "")
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not current_password:
            return render(
                request,
                "change_password.html",
                {"error": "Please enter your current password."}
            )

        if not new_password:
            return render(
                request,
                "change_password.html",
                {"error": "Please enter a new password."}
            )

        if len(new_password) < 8:
            return render(
                request,
                "change_password.html",
                {"error": "New password must contain at least 8 characters."}
            )

        if new_password != confirm_password:
            return render(
                request,
                "change_password.html",
                {"error": "New passwords do not match."}
            )

        if not request.user.check_password(current_password):
            return render(
                request,
                "change_password.html",
                {"error": "Current password is incorrect."}
            )

        if current_password == new_password:
            return render(
                request,
                "change_password.html",
                {"error": "New password must be different from your current password."}
            )

        request.user.set_password(new_password)
        request.user.save()

        # Keep user logged in after changing password
        from django.contrib.auth import authenticate, login

        user = authenticate(
            username=request.user.username,
            password=new_password
        )

        if user is not None:
            login(request, user)

        messages.success(
            request,
            "Password changed successfully! "
        )

        return redirect("profile")

    return render(request, "change_password.html")

def about(request):
    return render(request, "about.html")

def student_trip(request):
    return render(request, "student_trip.html")


def teenager_trip(request):
    return render(request, "teenager_trip.html")

def about(request):
    return render(request, "about.html")

def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        email_message = f"""
New Contact Us Message

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""

        try:
            send_mail(
                subject=f"Travel Vista Enquiry - {subject}",
                message=email_message,
                from_email="travelvistatourism2026@gmail.com",
                recipient_list=["travelvistatourism2026@gmail.com"],
                fail_silently=False,
            )

            messages.success(
                request,
                "Your message has been sent successfully! We will get back to you soon."
            )

        except Exception:
            messages.error(
                request,
                "Sorry, your message could not be sent. Please try again."
            )

        return render(request, "contact.html")

    return render(request, "contact.html")

def privacy_policy(request):
    return render(request, "privacy_policy.html")

def terms_conditions(request):
    return render(request, "terms_conditions.html")

def customer_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(request, "review_submitted.html")

    else:
        form = ReviewForm()

    return render(request, "customer_review.html", {"form": form})

def contact_success(request):
    return render(request, 'contact_success.html')