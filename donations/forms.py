from django import forms
from .models import FoodDonation


class FoodDonationForm(forms.ModelForm):

    class Meta:
        model = FoodDonation
        fields = [
            'food_name',
            'description',
            'category',
            'quantity',
            'location',
            'expiry_date',
        ]

        widgets = {
            'expiry_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }