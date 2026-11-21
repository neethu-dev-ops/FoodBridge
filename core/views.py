from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from donations.models import FoodDonation, DonationRequest
from django.utils import timezone

def home(request):
    return render(request, 'home.html')



@login_required
def donor_dashboard(request):

    profile = getattr(request.user, 'userprofile', None)

    if profile is None or profile.role != 'DONOR':
        return redirect('home')

    my_donations = FoodDonation.objects.filter(
        donor=request.user
    ).order_by('-created_at')

    return render(request, 'donor_dashboard.html', {
        'my_donations': my_donations
    })


@login_required
def ngo_dashboard(request):
    profile = getattr(request.user, 'userprofile', None)

    if profile is None or profile.role != 'NGO':
        return redirect('home')

    available_donations = FoodDonation.objects.filter(
    status='AVAILABLE',
    expiry_date__gt=timezone.now()
    )

    my_requests = DonationRequest.objects.filter(ngo=request.user)

    return render(request, 'ngo_dashboard.html', {
        'available_donations': available_donations,
        'my_requests': my_requests
    })