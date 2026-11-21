from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import FoodDonationForm
from .models import FoodDonation, DonationRequest, Pickup
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .ai_service import generate_food_description, suggest_food_category
from .forms import FoodDonationForm


@login_required
def add_donation(request):
    profile = getattr(request.user, 'userprofile', None)

    if profile is None or profile.role != 'DONOR':
        return redirect('home')

    if request.method == 'POST':
        form = FoodDonationForm(request.POST)

        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()

            return redirect('donor_dashboard')

    else:
        form = FoodDonationForm()

    return render(request, 'add_donation.html', {'form': form})

def available_food(request):
    from django.utils import timezone

    donations = FoodDonation.objects.filter(
        status='AVAILABLE',
        expiry_date__gt=timezone.now()
    )

    return render(request, 'available_food.html', {
        'donations': donations
    })

@login_required
def request_donation(request, donation_id):

    profile = getattr(request.user, 'userprofile', None)

    if profile is None or profile.role != 'NGO':
        return redirect('home')

    donation = get_object_or_404(FoodDonation, id=donation_id)

    if donation.status != 'AVAILABLE':
        messages.error(request, 'This food donation is no longer available.')
        return redirect('available_food')

    if donation.expiry_date <= timezone.now():
        messages.error(request, 'This food donation has expired.')
        return redirect('available_food')

    existing_request = DonationRequest.objects.filter(donation=donation, ngo=request.user,
        status__in=['PENDING', 'APPROVED']).exists()

    if existing_request:
        messages.error(request, 'You have already requested this food.')
        return redirect('available_food')


    if request.method == 'POST':
        quantity = request.POST.get('quantity')

        if not quantity or not quantity.isdigit():
            messages.error(request, 'Please enter a valid quantity.')
            return redirect('available_food')

        quantity = int(quantity)

        if quantity <= 0 or quantity > donation.quantity:
            messages.error(request, 'Invalid requested quantity.')
            return redirect('available_food')

        DonationRequest.objects.create(
            donation=donation,
            ngo=request.user,
            requested_quantity=quantity
        )

        return redirect('available_food')

    return render(request, 'request_donation.html', {
        'donation': donation
    })

@login_required
def donor_requests(request):

    profile = getattr(request.user, 'userprofile', None)

    if profile is None or profile.role != 'DONOR':
        return redirect('home')

    requests = DonationRequest.objects.filter(
        donation__donor=request.user
    )

    return render(request, 'donor_requests.html', {
        'requests': requests
    })

@login_required
@require_POST
def manage_donation_request(request, request_id):

    profile = getattr(request.user, 'userprofile', None)

    if profile is None or profile.role != 'DONOR':
        return redirect('home')

    donation_request = get_object_or_404(
        DonationRequest,
        id=request_id,
        donation__donor=request.user
    )

    action = request.POST.get('action')

    if donation_request.status != 'PENDING':
        messages.error(request, 'This request has already been processed.')
        return redirect('donor_requests')

    if action == 'approve':
        donation_request.status = 'APPROVED'
        donation_request.save()

        messages.success(request, 'Donation request approved successfully.')

    elif action == 'reject':
        donation_request.status = 'REJECTED'
        donation_request.save()

        messages.success(request, 'Donation request rejected.')

    return redirect('donor_requests')


@login_required
def schedule_pickup(request, request_id):

    profile = getattr(request.user, 'userprofile', None)

    if profile is None or profile.role != 'DONOR':
        return redirect('home')

    donation_request = get_object_or_404(
        DonationRequest,
        id=request_id,
        donation__donor=request.user,
        status='APPROVED'
    )

    if hasattr(donation_request, 'pickup'):
        messages.error(request, 'Pickup has already been scheduled.')
        return redirect('donor_requests')

    if request.method == 'POST':

        pickup_date = request.POST.get('pickup_date')
        pickup_location = request.POST.get('pickup_location')
        notes = request.POST.get('notes', '')

        parsed_date = parse_datetime(pickup_date) if pickup_date else None

        if not parsed_date or not pickup_location:
            messages.error(request, 'Please enter a valid pickup date and location.')

        else:
            if timezone.is_naive(parsed_date):
                parsed_date = timezone.make_aware(parsed_date)

            if parsed_date <= timezone.now():
                messages.error(request, 'Pickup date must be in the future.')

            else:
                Pickup.objects.create(
                    donation_request=donation_request,
                    pickup_date=parsed_date,
                    pickup_location=pickup_location,
                    notes=notes
                )

                messages.success(request, 'Pickup scheduled successfully!')
                return redirect('donor_requests')

    return render(request, 'schedule_pickup.html', {
        'donation_request': donation_request
    })


@login_required
@require_POST
def mark_pickup_collected(request, pickup_id):

    profile = getattr(request.user, 'userprofile', None)

    if profile is None or profile.role != 'NGO':
        return redirect('home')

    pickup = get_object_or_404(
        Pickup,
        id=pickup_id,
        donation_request__ngo=request.user
    )

    if pickup.status == 'SCHEDULED':
        pickup.status = 'COLLECTED'
        pickup.save()

        pickup.donation_request.status = 'COMPLETED'
        pickup.donation_request.save()

        pickup.donation_request.donation.status = 'PICKED_UP'
        pickup.donation_request.donation.save()

        messages.success(request, 'Food marked as collected successfully!')

    return redirect('ngo_dashboard')


from django.http import JsonResponse


@login_required
@require_POST
def generate_ai_description(request):

    profile = getattr(request.user, 'userprofile', None)

    if profile is None or profile.role != 'DONOR':
        return JsonResponse({'error': 'Access denied.'}, status=403)

    food_name = request.POST.get('food_name', '').strip()
    quantity = request.POST.get('quantity', '').strip()
    location = request.POST.get('location', '').strip()

    if not food_name or not quantity or not location:
        return JsonResponse({
            'error': 'Please enter food name, quantity and location first.'
        }, status=400)

    description = generate_food_description(
        food_name,
        quantity,
        location
    )

    if description.startswith('AI service error:') or description.startswith('Gemini API key is missing'):
        return JsonResponse({'error': description}, status=500)

    return JsonResponse({'description': description})

@login_required
@require_POST
def suggest_food_category_view(request):
    profile = getattr(request.user, 'userprofile', None)

    if profile is None or profile.role != 'DONOR':
        return JsonResponse({'error': 'Access denied.'}, status=403)

    food_name = request.POST.get('food_name', '').strip()

    if not food_name:
        return JsonResponse(
            {'error': 'Please enter a food name first.'},
            status=400
        )

    category = suggest_food_category(food_name)

    return JsonResponse({'category': category})

