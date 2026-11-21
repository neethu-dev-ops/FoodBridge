from django.db import models
from django.conf import settings


class FoodDonation(models.Model):

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('REQUESTED', 'Requested'),
        ('DONATED', 'Donated'),
        ('PICKED_UP', 'Picked Up'),
        ('EXPIRED', 'Expired'),
    ]

    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='food_donations'
    )

    food_name = models.CharField(max_length=150)

    description = models.TextField()

    CATEGORY_CHOICES = [
    ('COOKED', 'Cooked Meals'),
    ('FRUITS', 'Fruits & Vegetables'),
    ('BAKERY', 'Bakery Items'),
    ('PACKAGED', 'Packaged Food'),
    ('DAIRY', 'Dairy Products'),
    ('OTHER', 'Other'),
    ]

    category = models.CharField(
    max_length=20,
    choices=CATEGORY_CHOICES,
    default='OTHER'
    )

    quantity = models.PositiveIntegerField()

    location = models.CharField(max_length=200)

    expiry_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AVAILABLE'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.food_name

class DonationRequest(models.Model):

    REQUEST_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    ]

    donation = models.ForeignKey(
        FoodDonation,
        on_delete=models.CASCADE,
        related_name='requests'
    )

    ngo = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donation_requests'
    )

    requested_quantity = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=REQUEST_STATUS,
        default='PENDING'
    )

    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ngo.username} - {self.donation.food_name}"

class Pickup(models.Model):

    PICKUP_STATUS = [
        ('SCHEDULED', 'Scheduled'),
        ('COLLECTED', 'Collected'),
        ('CANCELLED', 'Cancelled'),
    ]

    donation_request = models.OneToOneField(
        DonationRequest,
        on_delete=models.CASCADE,
        related_name='pickup'
    )

    pickup_date = models.DateTimeField()

    pickup_location = models.CharField(max_length=200)

    status = models.CharField(
        max_length=20,
        choices=PICKUP_STATUS,
        default='SCHEDULED'
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Pickup - {self.donation_request.donation.food_name}"