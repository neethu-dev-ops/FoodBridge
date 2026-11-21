from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_donation, name='add_donation'),
    path('available/', views.available_food, name='available_food'),
    path('request/<int:donation_id>/', views.request_donation, name='request_donation'),
    path('donor-requests/', views.donor_requests, name='donor_requests'),
    path('manage-request/<int:request_id>/', views.manage_donation_request, name='manage_donation_request'),
    path('schedule-pickup/<int:request_id>/', views.schedule_pickup, name='schedule_pickup'),
    path('mark-collected/<int:pickup_id>/', views.mark_pickup_collected, name='mark_pickup_collected'),
    path('generate-ai-description/', views.generate_ai_description, name='generate_ai_description'),
    path('suggest-food-category/', views.suggest_food_category_view, name='suggest_food_category'),
]