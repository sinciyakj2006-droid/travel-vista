from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    YES_NO_CHOICES = [
        (False, "No"),
        (True, "Yes"),
    ]

    # =====================================================
    # SPECIAL TRAVEL FEATURES
    # =====================================================

    guide_required = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda x: x == "True",
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    photography_required = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda x: x == "True",
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    google_map_required = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda x: x == "True",
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    hospitality_required = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda x: x == "True",
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    airbnb_required = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda x: x == "True",
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    gps_tracking_required = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda x: x == "True",
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    travel_with_strangers = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=lambda x: x == "True",
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    # =====================================================
    # KIDS FEATURES
    # =====================================================

    kids_features = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    # =====================================================
    # TRAVELING METHOD
    # =====================================================

    
    # =====================================================
    # PAYMENT METHOD
    # =====================================================

    payment_method = forms.ChoiceField(
        choices=[
            ("", "Select Payment Method"),
            ("UPI", " UPI"),
            ("CARD", " Card"),
            ("CASH", " Cash on Arrival"),
        ],
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        model = Booking

        fields = [
            "username",
            "full_name",
            "email",
            "phone",
            "address",
            "travel_date",
            "number_of_people",
          
            "guide_required",
            "photography_required",
            "google_map_required",
            "hospitality_required",
            "airbnb_required",
            "gps_tracking_required",
            "travel_with_strangers",
            "extra_details",
            "payment_method",
        ]

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your username"
                }
            ),

            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your full name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter 10 digit phone number",
                    "maxlength": "10"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter your full address"
                }
            ),

            "travel_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "number_of_people": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Number of people"
                }
            ),

            "extra_details": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Any extra details or special requests?"
                }
            ),
        }

    # =====================================================
    # USERNAME VALIDATION
    # =====================================================

    def clean_username(self):

        username = self.cleaned_data.get(
            "username",
            ""
        ).strip()

        if not username:
            raise forms.ValidationError(
                "Username is required."
            )

        if len(username) < 3:
            raise forms.ValidationError(
                "Username must contain at least 3 characters."
            )

        if not username.replace(
            "_",
            ""
        ).isalnum():

            raise forms.ValidationError(
                "Username can contain only letters, numbers and underscore."
            )

        return username

    # =====================================================
    # EMAIL VALIDATION
    # =====================================================

    def clean_email(self):

        email = self.cleaned_data.get(
            "email",
            ""
        ).strip()

        if not email:
            raise forms.ValidationError(
                "Email is required."
            )

        if (
            "@" not in email
            or "." not in email.split("@")[-1]
        ):

            raise forms.ValidationError(
                "Please enter a valid email address."
            )

        return email

    # =====================================================
    # PHONE VALIDATION
    # =====================================================

    def clean_phone(self):

        phone = self.cleaned_data.get(
            "phone",
            ""
        ).strip()

        if not phone:
            raise forms.ValidationError(
                "Phone number is required."
            )

        if not phone.isdigit():

            raise forms.ValidationError(
                "Phone number must contain only digits."
            )

        if len(phone) != 10:

            raise forms.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        if phone[0] not in "6789":

            raise forms.ValidationError(
                "Please enter a valid Indian mobile number."
            )

        return phone

    # =====================================================
    # NUMBER OF PEOPLE VALIDATION
    # =====================================================

    def clean_number_of_people(self):

        number = self.cleaned_data.get(
            "number_of_people"
        )

        if number is None or number < 1:

            raise forms.ValidationError(
                "Number of people must be at least 1."
            )

        return number

    

    # =====================================================
    # PAYMENT VALIDATION
    # =====================================================

    def clean_payment_method(self):

        payment_method = self.cleaned_data.get(
            "payment_method"
        )

        if not payment_method:

            raise forms.ValidationError(
                "Please select a payment method."
            )

        return payment_method