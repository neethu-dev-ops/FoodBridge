from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                organization_name=form.cleaned_data['organization_name']
            )

            return redirect('home')

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            profile = getattr(user, 'userprofile', None)

            if profile and profile.role == 'DONOR':
                return redirect('donor_dashboard')

            elif profile and profile.role == 'NGO':
                return redirect('ngo_dashboard')

            else:
                return redirect('home')

        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

