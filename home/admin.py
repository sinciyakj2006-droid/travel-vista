from django.contrib import admin
from .models import Destination, DestinationImage, TourPackage


# =====================================================
# DESTINATION IMAGE INLINE
# =====================================================

class DestinationImageInline(admin.TabularInline):

    model = DestinationImage

    extra = 3

    max_num = 10

    fields = (
        "image",
    )


# =====================================================
# DESTINATION ADMIN
# =====================================================

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "location",
        "budget",
        "mood",
        "season",
        "is_available",
    )

    list_filter = (
        "mood",
        "season",
        "is_available",
    )

    search_fields = (
        "name",
        "location",
        "activities",
    )

    ordering = (
        "name",
    )

    inlines = [
        DestinationImageInline
    ]


# =====================================================
# DESTINATION IMAGE ADMIN
# =====================================================

@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):

    list_display = (
        "destination",
        "image",
        "created_at",
    )

    search_fields = (
        "destination__name",
    )


# =====================================================
# TOUR PACKAGE ADMIN
# =====================================================

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "destination",
        "duration",
        "price",
        "is_available",
        "created_at",
    )

    list_filter = (
        "destination",
        "is_available",
    )

    search_fields = (
        "name",
        "destination__name",
    )

    ordering = (
        "-created_at",
    )

