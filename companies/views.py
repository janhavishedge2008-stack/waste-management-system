from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import CompanyWasteRequest, WasteType
from .forms import CompanyWasteRequestForm
from users.models import Notification


@login_required
def company_dashboard(request):
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('home')

    from .models import CollectedWaste

    all_requests = CompanyWasteRequest.objects.filter(company=request.user)
    pending = all_requests.filter(status='pending').count()
    approved = all_requests.filter(status='approved').count()
    fulfilled = all_requests.filter(status='fulfilled').count()
    cancelled = all_requests.filter(status='cancelled').count()

    waste_breakdown = (
        all_requests.values('waste_type__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Live inventory — what's available right now
    live_inventory = CollectedWaste.objects.select_related('waste_type').filter(
        available_quantity__gt=0
    ).order_by('-available_quantity')

    unread_notifs = Notification.objects.filter(user=request.user, is_read=False).count()
    recent_notifs = Notification.objects.filter(user=request.user)[:5]

    context = {
        'requests': all_requests.order_by('-created_at'),
        'total': all_requests.count(),
        'pending': pending,
        'approved': approved,
        'fulfilled': fulfilled,
        'cancelled': cancelled,
        'waste_breakdown': list(waste_breakdown),
        'live_inventory': live_inventory,
        'unread_notifs': unread_notifs,
        'recent_notifs': recent_notifs,
    }
    return render(request, 'companies/dashboard.html', context)


@login_required
def create_waste_request(request):
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('home')

    if request.method == 'POST':
        form = CompanyWasteRequestForm(request.POST)
        if form.is_valid():
            waste_request = form.save(commit=False)
            waste_request.company = request.user
            waste_request.save()
            Notification.objects.create(
                user=request.user,
                message=f'Waste request for {waste_request.waste_type.name} submitted successfully!',
                notif_type='company',
                link='/companies/dashboard/'
            )
            messages.success(request, 'Waste request submitted successfully!')
            return redirect('company_dashboard')
    else:
        form = CompanyWasteRequestForm()
    return render(request, 'companies/create_request.html', {'form': form})


@login_required
def available_waste(request):
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('home')

    from .models import CollectedWaste
    from django.db.models import Sum
    from pickups.models import PickupRequest

    # Waste with available stock from completed pickups
    inventory = CollectedWaste.objects.select_related('waste_type').filter(
        available_quantity__gt=0
    ).order_by('-available_quantity')

    # Also show waste types with no stock yet (so companies know what we handle)
    all_waste_types = WasteType.objects.all()

    # Stats
    total_collected = CollectedWaste.objects.aggregate(t=Sum('total_quantity'))['t'] or 0
    total_available = CollectedWaste.objects.aggregate(t=Sum('available_quantity'))['t'] or 0
    completed_pickups = PickupRequest.objects.filter(status='completed').count()

    context = {
        'inventory': inventory,
        'all_waste_types': all_waste_types,
        'total_collected': total_collected,
        'total_available': total_available,
        'completed_pickups': completed_pickups,
    }
    return render(request, 'companies/available_waste.html', context)


def company_tieup_page(request):
    return render(request, 'companies/tieup.html')
