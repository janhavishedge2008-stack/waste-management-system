from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('register-company/', views.register_company, name='register_company'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('notifications/read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('api/notifications/', views.notifications_api, name='notifications_api'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
]
