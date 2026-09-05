from django.db import models
from home.models import TourPackage


class Booking(models.Model):

    # =====================================================
    # PACKAGE
    # =====================================================

    package = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,
        blank=True
    )

    # =====================================================
    # CUSTOMER DETAILS
    # =====================================================

    full_name = models.CharField(max_length=100)

    username = models.CharField(max_length=50)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    address = models.TextField()

    # =====================================================
    # TRAVEL DETAILS
    # =====================================================

    travel_date = models.DateField()

    number_of_people = models.PositiveIntegerField(default=1)

    TRAVEL_METHOD_CHOICES = [
        ("BUS", " Bus"),
        ("TRAIN", " Train"),
        ("FLIGHT", " Flight"),
        ("CAR", "Car"),
    ]

    travel_method = models.CharField(
        max_length=20,
        choices=TRAVEL_METHOD_CHOICES,
        default="BUS"
    )

    # =====================================================
    # SPECIAL TRAVEL FEATURES
    # =====================================================

    guide_required = models.BooleanField(default=False)

    photography_required = models.BooleanField(default=False)

    google_map_required = models.BooleanField(default=False)

    hospitality_required = models.BooleanField(default=False)

    airbnb_required = models.BooleanField(default=False)

    gps_tracking_required = models.BooleanField(default=False)

    travel_with_strangers = models.BooleanField(default=False)

    # =====================================================
    # KIDS-FRIENDLY FEATURES
    # =====================================================

    kids_features = models.TextField(
        blank=True,
        null=True
    )

    # =====================================================
    # EXTRA DETAILS
    # =====================================================

    extra_details = models.TextField(
        blank=True,
        null=True
    )

    # =====================================================
    # GPS TRACKING
    # =====================================================

    tracking_active = models.BooleanField(default=False)

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    location_updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # =====================================================
    # PAYMENT METHOD
    # =====================================================

    PAYMENT_METHOD_CHOICES = [
        ("UPI", "UPI"),
        ("CARD", "Card"),
        ("CASH", "Cash on Arrival"),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="UPI"
    )

    # =====================================================
    # PAYMENT STATUS
    # =====================================================

    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
    ]

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING"
    )

    # =====================================================
    # BOOKING CREATED TIME
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================================
    # DISPLAY NAME
    # =====================================================

    def __str__(self):

        if self.package:

            return f"{self.full_name} - {self.package.name}"

        return f"{self.full_name} - Destination Booking"
