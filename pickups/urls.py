from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_pickup, name='create_pickup'),
    path('history/', views.pickup_history, name='pickup_history'),
    path('detail/<int:pk>/', views.pickup_detail, name='pickup_detail'),
    path('cancel/<int:pk>/', views.cancel_pickup, name='cancel_pickup'),
    # Worker
    path('worker/dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('worker/update/<int:pk>/<str:new_status>/', views.worker_update_status, name='worker_update_status'),
    # Analytics API
    path('api/analytics/', views.analytics_api, name='analytics_api'),
]
