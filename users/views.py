from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .forms import UserRegistrationForm, CompanyRegistrationForm, ProfileEditForm
from .models import User, Notification
from pickups.models import PickupRequest


def send_otp_email(user):
    """Send OTP verification email."""
    from django.core.mail import send_mail
    from django.conf import settings
    otp = user.generate_otp()
    try:
        send_mail(
            subject='EcoWaste — Email Verification OTP',
            message=f'Hi {user.username},\n\nYour OTP code is: {otp}\n\nThis code expires in 10 minutes.\n\n— EcoWaste Team',
            from_email=settings.EMAIL_HOST_USER or 'noreply@ecowaste.com',
            recipient_list=[user.email],
            fail_silently=True,
        )
    except Exception:
        pass  # Email not configured — OTP still stored in DB


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'regular'
            user.is_email_verified = False
            user.save()
            send_otp_email(user)
            Notification.objects.create(
                user=user,
                message='Welcome to EcoWaste! Schedule your first pickup to earn 10 reward points.',
                notif_type='system',
                link='/pickups/create/'
            )
            login(request, user)
            messages.success(request, 'Registration successful! Check your email for OTP verification.')
            return redirect('verify_email')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'user_type': 'User'})


def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'company'
            user.is_email_verified = False
            user.save()
            send_otp_email(user)
            Notification.objects.create(
                user=user,
                message='Welcome! Your company account is ready. Start by creating a waste request.',
                notif_type='system',
                link='/companies/create-request/'
            )
            login(request, user)
            messages.success(request, 'Company registration successful! Please verify your email.')
            return redirect('verify_email')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'user_type': 'Company'})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.user_type == 'company':
                return redirect('company_dashboard')
            elif user.user_type == 'worker':
                return redirect('worker_dashboard')
            elif user.user_type == 'admin' or user.is_staff:
                return redirect('admin:index')
            return redirect('user_dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


@login_required
def verify_email(request):
    if request.user.is_email_verified:
        return redirect('user_dashboard')
    if request.method == 'POST':
        otp = request.POST.get('otp', '').strip()
        if request.user.is_otp_valid(otp):
            request.user.is_email_verified = True
            request.user.otp_code = ''
            request.user.save(update_fields=['is_email_verified', 'otp_code'])
            messages.success(request, 'Email verified successfully!')
            if request.user.user_type == 'company':
                return redirect('company_dashboard')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
    return render(request, 'users/verify_email.html')


@login_required
def resend_otp(request):
    send_otp_email(request.user)
    messages.success(request, 'A new OTP has been sent to your email.')
    return redirect('verify_email')


@login_required
def user_dashboard(request):
    pickups = PickupRequest.objects.filter(user=request.user).order_by('-created_at')
    unread_notifs = Notification.objects.filter(user=request.user, is_read=False).count()
    recent_notifs = Notification.objects.filter(user=request.user)[:5]
    level, level_icon = request.user.get_level()

    completed = pickups.filter(status='completed').count()
    pending = pickups.filter(status='pending').count()
    cancelled = pickups.filter(status='cancelled').count()

    context = {
        'pickups': pickups,
        'unread_notifs': unread_notifs,
        'recent_notifs': recent_notifs,
        'level': level,
        'level_icon': level_icon,
        'completed': completed,
        'pending': pending,
        'cancelled': cancelled,
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_dashboard')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'user_dashboard'))


def leaderboard(request):
    top_users = User.objects.filter(
        user_type='regular', is_active=True
    ).order_by('-reward_points')[:20]
    context = {'top_users': top_users}
    return render(request, 'users/leaderboard.html', context)


@login_required
def notifications_api(request):
    from django.http import JsonResponse
    from django.utils.timesince import timesince
    notifs = Notification.objects.filter(user=request.user)[:8]
    unread = Notification.objects.filter(user=request.user, is_read=False).count()
    icon_map = {'pickup': 'truck', 'reward': 'star', 'system': 'bell', 'company': 'building'}
    data = {
        'unread': unread,
        'notifications': [
            {
                'message': n.message,
                'type': n.notif_type,
                'icon': icon_map.get(n.notif_type, 'bell'),
                'is_read': n.is_read,
                'link': n.link,
                'time': timesince(n.created_at) + ' ago',
            }
            for n in notifs
        ]
    }
    return JsonResponse(data)
