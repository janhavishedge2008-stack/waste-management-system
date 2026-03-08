from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, CompanyRegistrationForm
from pickups.models import PickupRequest

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'regular'
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('user_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'user_type': 'User'})

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'company'
            user.save()
            login(request, user)
            messages.success(request, 'Company registration successful!')
            return redirect('company_dashboard')
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
            elif user.user_type == 'admin' or user.is_staff:
                return redirect('admin:index')
            return redirect('user_dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')

@login_required
def user_dashboard(request):
    pickups = PickupRequest.objects.filter(user=request.user).order_by('-created_at')
    context = {'pickups': pickups, 'user': request.user}
    return render(request, 'users/dashboard.html', context)
