from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.company_dashboard, name='company_dashboard'),
    path('create-request/', views.create_waste_request, name='create_waste_request'),
    path('available-waste/', views.available_waste, name='available_waste'),
    path('tieup/', views.company_tieup_page, name='company_tieup'),
]
