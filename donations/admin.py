from django.contrib import admin
from .models import FoodDonation, DonationRequest, Pickup

admin.site.register(FoodDonation)
admin.site.register(DonationRequest)
admin.site.register(Pickup)