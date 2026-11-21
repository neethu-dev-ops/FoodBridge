from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('donor-dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('ngo-dashboard/', views.ngo_dashboard, name='ngo_dashboard'),
]