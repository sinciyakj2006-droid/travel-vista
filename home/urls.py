from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/change-password/", views.change_password, name="change_password"),

    path("destinations/", views.destination_list, name="destination_list"),
    path("destinations/<int:pk>/",
         views.destination_detail,
         name="destination_detail"),

    path("about/", views.about, name="about"),

    path("mood-planner/", views.mood_planner, name="mood_planner"),

    path("tour-packages/", views.tour_packages, name="tour_packages"),
    path("tour-packages/<int:pk>/",
         views.tour_package_detail,
         name="tour_package_detail"),

    # TYPES OF TRAVELS
    path("trip-with-strangers/",
         views.strangers_trip,
         name="strangers_trip"),

    path("solo-trip/",
         views.solo_trip,
         name="solo_trip"),

    path("kids-trip/",
         views.kids_trip,
         name="kids_trip"),

    path("my-bookings/",
         views.my_bookings,
         name="my_bookings"),

    path("about/", views.about, name="about"),

    path("contact/", views.contact, name="contact"),

    path(
    'contact/success/',
    views.contact_success,
    name='contact_success'
),

    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),

    path(
    "terms-and-conditions/",
    views.terms_conditions,
    name="terms_conditions"
),

path("customer-review/", views.customer_review, name="customer_review"),
]