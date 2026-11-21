from django.db import models
from django.conf import settings


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('DONOR', 'Donor'),
        ('NGO', 'NGO'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(max_length=15)

    address = models.TextField()

    organization_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username