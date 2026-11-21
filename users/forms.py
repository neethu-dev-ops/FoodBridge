from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES
    )

    phone = forms.CharField(max_length=15)

    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3})
    )

    organization_name = forms.CharField(
        max_length=150,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]