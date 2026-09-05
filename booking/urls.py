from django.urls import path
from . import views


urlpatterns = [

    # ==========================================
    # PACKAGE BOOKING
    # ==========================================

    path(
        "book/<int:pk>/",
        views.create_booking,
        name="create_booking"
    ),

    # ==========================================
    # DESTINATION BOOKING
    # ==========================================

    path(
        "destination/<int:pk>/",
        views.create_destination_booking,
        name="create_destination_booking"
    ),

    # ==========================================
    # GPS LOCATION UPDATE
    # ==========================================

    path(
        "location/<int:pk>/",
        views.update_location,
        name="update_location"
    ),

    # ==========================================
    # GET CURRENT GPS LOCATION
    # ==========================================

    path(
        "location/<int:pk>/current/",
        views.get_location,
        name="get_location"
    ),

    # ==========================================
    # ADMIN TRACKING
    # ==========================================

    path(
        "admin-tracking/",
        views.admin_tracking,
        name="admin_tracking"
    ),

    # ==========================================
    # BOOKING SUCCESS
    # ==========================================

    path(
        "success/",
        views.booking_success,
        name="booking_success"
    ),
]