from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["name", "email", "rating", "review", "image"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email"
                }
            ),

            "rating": forms.Select(
                choices=[
                    (1, "1 Star"),
                    (2, "2 Stars"),
                    (3, "3 Stars"),
                    (4, "4 Stars"),
                    (5, "5 Stars"),
                ],
                attrs={
                    "class": "form-control"
                }
            ),

            "review": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Write your travel experience..."
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".jpg,.jpeg,.png,.webp"
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()

        if not name:
            raise forms.ValidationError("Name is required.")

        if len(name) < 2:
            raise forms.ValidationError(
                "Name must contain at least 2 characters."
            )

        if name.isdigit():
            raise forms.ValidationError(
                "Name cannot contain only numbers."
            )

        return name

    def clean_review(self):
        review = self.cleaned_data.get("review", "").strip()

        if not review:
            raise forms.ValidationError("Please write your review.")

        if len(review) < 10:
            raise forms.ValidationError(
                "Review must contain at least 10 characters."
            )

        return review