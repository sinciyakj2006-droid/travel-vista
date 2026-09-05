from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from home.models import TourPackage, Destination
from .forms import BookingForm
from .models import Booking


# =========================================================
# PACKAGE BOOKING
# =========================================================

def create_booking(request, pk):

    package = get_object_or_404(
        TourPackage,
        pk=pk,
        is_available=True
    )

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            booking.package = package

            # =================================================
            # KIDS-FRIENDLY FEATURES
            # =================================================

            kids_features = request.POST.getlist("kids_features")

            booking.kids_features = ", ".join(kids_features)

            booking.save()

            # =================================================
            # BOOKING CONFIRMATION EMAIL
            # =================================================

            send_mail(
                subject="Booking Confirmed - Travel Vista",

                message=f"""
Hello {booking.full_name},

Your booking has been confirmed successfully! 

Booking Details
-------------------------
Package: {booking.package.name}
Destination: {booking.package.destination.name}
Travel Date: {booking.travel_date}
Number of People: {booking.number_of_people}
Payment Method: {booking.get_payment_method_display()}
Kids-Friendly Features: {booking.kids_features or "None selected"}

Thank you for choosing Travel Vista.

Have a wonderful journey! 

Regards,
Travel Vista
""",

                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.email],
                fail_silently=False,
            )

            return render(
                request,
                "booking/booking_success.html",
                {
                    "booking_id": booking.pk
                }
            )

    else:

        form = BookingForm()

    return render(
        request,
        "booking/booking_form.html",
        {
            "package": package,
            "form": form
        }
    )


# =========================================================
# DESTINATION BOOKING
# =========================================================

def create_destination_booking(request, pk):

    destination = get_object_or_404(
        Destination,
        pk=pk,
        is_available=True
    )

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            # Destination booking
            booking.package = None

            # =================================================
            # KIDS-FRIENDLY FEATURES
            # =================================================

            kids_features = request.POST.getlist("kids_features")

            booking.kids_features = ", ".join(kids_features)

            booking.save()

            # =================================================
            # BOOKING CONFIRMATION EMAIL
            # =================================================

            send_mail(
                subject="Booking Confirmed - Travel Vista",

                message=f"""
Hello {booking.full_name},

Your destination booking has been confirmed successfully! 

Booking Details
-------------------------
Destination: {destination.name}
Travel Date: {booking.travel_date}
Number of People: {booking.number_of_people}
Payment Method: {booking.get_payment_method_display()}
Kids-Friendly Features: {booking.kids_features or "None selected"}

Thank you for choosing Travel Vista.

Have a wonderful journey! 

Regards,
Travel Vista
""",

                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.email],
                fail_silently=False,
            )

            return render(
                request,
                "booking/booking_success.html",
                {
                    "booking_id": booking.pk
                }
            )

    else:

        form = BookingForm()

    return render(
        request,
        "booking/booking_form.html",
        {
            "destination": destination,
            "package": None,
            "form": form
        }
    )


# =========================================================
# BOOKING SUCCESS
# =========================================================

def booking_success(request):

    return render(
        request,
        "booking/booking_success.html"
    )


# =========================================================
# GPS LOCATION UPDATE
# =========================================================

@require_POST
def update_location(request, pk):

    try:

        booking = Booking.objects.get(pk=pk)

    except Booking.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "message": "Booking not found."
            },
            status=404
        )

    latitude = request.POST.get("latitude")
    longitude = request.POST.get("longitude")

    if not latitude or not longitude:

        return JsonResponse(
            {
                "success": False,
                "message": "Location coordinates are required."
            },
            status=400
        )

    try:

        booking.latitude = float(latitude)
        booking.longitude = float(longitude)

    except ValueError:

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid location coordinates."
            },
            status=400
        )

    # Activate GPS tracking
    booking.tracking_active = True

    # Save latest location update time
    booking.location_updated_at = timezone.now()

    booking.save(
        update_fields=[
            "latitude",
            "longitude",
            "tracking_active",
            "location_updated_at",
        ]
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Location updated successfully."
        }
    )


# =========================================================
# ADMIN GPS TRACKING DASHBOARD
# =========================================================

def admin_tracking(request):

    bookings = Booking.objects.filter(
        tracking_active=True
    ).select_related(
        "package",
        "package__destination"
    ).order_by(
        "-location_updated_at"
    )

    return render(
        request,
        "booking/admin_tracking.html",
        {
            "bookings": bookings
        }
    )


# =========================================================
# GET CURRENT GPS LOCATION
# =========================================================

def get_location(request, pk):

    try:

        booking = Booking.objects.get(pk=pk)

    except Booking.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "message": "Booking not found."
            },
            status=404
        )

    if booking.latitude is None or booking.longitude is None:

        return JsonResponse(
            {
                "success": True,
                "tracking_active": booking.tracking_active,
                "latitude": None,
                "longitude": None,
                "updated_at": None,
            }
        )

    return JsonResponse(
        {
            "success": True,
            "tracking_active": booking.tracking_active,
            "latitude": float(booking.latitude),
            "longitude": float(booking.longitude),
            "updated_at": (
                booking.location_updated_at.isoformat()
                if booking.location_updated_at
                else None
            ),
        }
    )