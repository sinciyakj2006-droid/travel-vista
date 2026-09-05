from django.contrib import admin
from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.utils.html import format_html

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    # =====================================================
    # BOOKING LIST
    # =====================================================

    list_display = (
        "full_name",
        "email",
        "phone",
        "get_destination",
        "travel_date",
        "number_of_people",
        "travel_method",
        "payment_method",
        "payment_status",
        "tracking_status",
        "location_updated_at",
        "created_at",
    )

    # =====================================================
    # FILTERS
    # =====================================================

    list_filter = (
        "travel_method",
        "payment_method",
        "payment_status",
        "tracking_active",
        "travel_date",
        "created_at",
    )

    # =====================================================
    # SEARCH
    # =====================================================

    search_fields = (
        "full_name",
        "email",
        "phone",
        "username",
        "kids_features",
        "travel_method",
    )

    # =====================================================
    # ORDERING
    # =====================================================

    ordering = ("-created_at",)

    # =====================================================
    # READ ONLY FIELDS
    # =====================================================

    readonly_fields = (
        "created_at",
        "latitude",
        "longitude",
        "location_updated_at",
    )

    # =====================================================
    # FIELDSETS
    # =====================================================

    fieldsets = (

        # -------------------------------------------------
        # CUSTOMER DETAILS
        # -------------------------------------------------

        (
            " Customer Details",
            {
                "fields": (
                    "username",
                    "full_name",
                    "email",
                    "phone",
                    "address",
                )
            }
        ),

        # -------------------------------------------------
        # TRAVEL DETAILS
        # -------------------------------------------------

        (
            " Travel Details",
            {
                "fields": (
                    "package",
                    "travel_date",
                    "number_of_people",
                    "travel_method",
                )
            }
        ),

        # -------------------------------------------------
        # SPECIAL TRAVEL FEATURES
        # -------------------------------------------------

        (
            " Special Travel Features",
            {
                "fields": (
                    "guide_required",
                    "photography_required",
                    "google_map_required",
                    "hospitality_required",
                    "airbnb_required",
                    "gps_tracking_required",
                    "travel_with_strangers",
                    "extra_details",
                )
            }
        ),

        # -------------------------------------------------
        # KIDS-FRIENDLY FEATURES
        # -------------------------------------------------

        (
            "Kids-Friendly Features",
            {
                "fields": (
                    "kids_features",
                )
            }
        ),

        # -------------------------------------------------
        # GPS TRACKING
        # -------------------------------------------------

        (
            " GPS Tracking",
            {
                "fields": (
                    "tracking_active",
                    "latitude",
                    "longitude",
                    "location_updated_at",
                )
            }
        ),

        # -------------------------------------------------
        # PAYMENT DETAILS
        # -------------------------------------------------

        (
            " Payment Details",
            {
                "fields": (
                    "payment_method",
                    "payment_status",
                )
            }
        ),

        # -------------------------------------------------
        # BOOKING INFORMATION
        # -------------------------------------------------

        (
            " Booking Information",
            {
                "fields": (
                    "created_at",
                )
            }
        ),
    )

    # =====================================================
    # DESTINATION
    # =====================================================

    @admin.display(description="Destination")
    def get_destination(self, obj):

        if obj.package:
            return obj.package.destination.name

        return "Destination Booking"

    # =====================================================
    # GPS STATUS
    # =====================================================

    @admin.display(description="GPS STATUS")
    def tracking_status(self, obj):

        if obj.tracking_active:

            return format_html(
                '<a href="/admin/booking/booking/{}/live-location/" '
                'style="color:#198754;font-weight:bold;">'
                '{}'
                '</a>',
                obj.pk,
                "🟢 Active"
            )

        return format_html(
            '<span style="color:#777;">{}</span>',
            "⚪ Not Active"
        )

    # =====================================================
    # CUSTOM ADMIN URL
    # =====================================================

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:booking_id>/live-location/",
                self.admin_site.admin_view(
                    self.live_location
                ),
                name="booking_live_location",
            ),
        ]

        return custom_urls + urls

    # =====================================================
    # LIVE LOCATION PAGE
    # =====================================================

    def live_location(self, request, booking_id):

        booking = get_object_or_404(
            Booking,
            pk=booking_id
        )

        context = {
            **self.admin_site.each_context(request),

            "title": "Live Customer Location",

            "booking": booking,
        }

        return render(
            request,
            "booking/admin_live_location.html",
            context,
        )