from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_pickup, name='create_pickup'),
    path('history/', views.pickup_history, name='pickup_history'),
    path('detail/<int:pk>/', views.pickup_detail, name='pickup_detail'),
    path('cancel/<int:pk>/', views.cancel_pickup, name='cancel_pickup'),
]
