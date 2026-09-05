from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# =====================================================
# VALIDATION FUNCTIONS
# =====================================================

def validate_destination_name(value):
    value = value.strip()

    if len(value) < 2:
        raise ValidationError(
            "Destination name must contain at least 2 characters."
        )

    if value.isdigit():
        raise ValidationError(
            "Destination name cannot contain only numbers."
        )


def validate_location(value):
    value = value.strip()

    if len(value) < 2:
        raise ValidationError(
            "Location must contain at least 2 characters."
        )


def validate_description(value):
    value = value.strip()

    if len(value) < 30:
        raise ValidationError(
            "Description must contain at least 30 characters."
        )


def validate_activities(value):
    value = value.strip()

    if len(value) < 3:
        raise ValidationError(
            "Please enter at least one valid activity."
        )


def validate_image(image):
    if image:
        allowed_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        ]

        filename = image.name.lower()

        if not any(
            filename.endswith(ext)
            for ext in allowed_extensions
        ):
            raise ValidationError(
                "Please upload a JPG, JPEG, PNG or WEBP image."
            )

        if image.size > 5 * 1024 * 1024:
            raise ValidationError(
                "Image size must be less than 5 MB."
            )


# =====================================================
# DESTINATION MODEL
# =====================================================

class Destination(models.Model):

    MOOD_CHOICES = [
        ("Relax", "Relax"),
        ("Adventure", "Adventure"),
        ("Family", "Family"),
        ("Romantic", "Romantic"),
        ("Nature", "Nature"),
        ("Student", "Student"),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            validate_destination_name
        ],
    )

    location = models.CharField(
        max_length=150,
        validators=[
            validate_location
        ],
    )

    description = models.TextField(
        validators=[
            validate_description
        ],
    )

    image = models.ImageField(
        upload_to="destinations/",
        validators=[
            validate_image
        ],
    )

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal("1.00"),
                message="Budget must be greater than ₹0."
            )
        ],
    )

    season = models.CharField(
        max_length=100,
    )

    activities = models.CharField(
        max_length=300,
        validators=[
            validate_activities
        ],
    )

    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES,
    )

    is_available = models.BooleanField(
        default=True
    )

    guide_available = models.BooleanField(
        default=False
    )

    photography_available = models.BooleanField(
        default=False
    )

    google_map_available = models.BooleanField(
        default=False
    )

    hospitality_available = models.BooleanField(
        default=False
    )

    airbnb_available = models.BooleanField(
        default=False
    )

    gps_tracking_available = models.BooleanField(
        default=False
    )

    travel_with_strangers = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


# =====================================================
# DESTINATION GALLERY IMAGES
# =====================================================

class DestinationImage(models.Model):

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="gallery_images"
    )

    image = models.ImageField(
        upload_to="destinations/gallery/",
        validators=[
            validate_image
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.destination.name} - Image"

        

# =====================================================
# TOUR PACKAGE MODEL
# =====================================================

class TourPackage(models.Model):

    name = models.CharField(max_length=150)

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="tour_packages"
    )

    duration = models.CharField(max_length=50)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal("1.00"),
                message="Price must be greater than ₹0."
            )
        ]
    )

    description = models.TextField()

    included_services = models.TextField(
        help_text="Example: Hotel, Breakfast, Transport, Guide"
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    review = models.TextField(max_length=1000)
    image = models.ImageField(
        upload_to="reviews/",
        blank=True,
        null=True
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}/5"