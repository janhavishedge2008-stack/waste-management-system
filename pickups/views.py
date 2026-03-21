from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import PickupRequest
from .forms import PickupRequestForm
from users.models import Notification, User


def auto_assign_company(pickup):
    """Auto-assign a company that handles this waste type."""
    from companies.models import CompanyWasteRequest
    # Find companies that have requested this waste type (i.e., they handle it)
    company_ids = CompanyWasteRequest.objects.filter(
        waste_type=pickup.waste_type,
        status__in=['pending', 'approved']
    ).values_list('company_id', flat=True).distinct()

    if company_ids:
        company = User.objects.filter(
            id__in=company_ids, user_type='company', is_active=True
        ).first()
        if company:
            pickup.assigned_company = company
            return company
    # Fallback: assign any active company
    company = User.objects.filter(user_type='company', is_active=True).first()
    if company:
        pickup.assigned_company = company
    return company


@login_required
def create_pickup(request):
    if request.method == 'POST':
        form = PickupRequestForm(request.POST, request.FILES)
        if form.is_valid():
            pickup = form.save(commit=False)
            pickup.user = request.user

            # Auto-assign company
            auto_assign_company(pickup)

            # Suggest waste category based on waste type name if not provided
            if not pickup.waste_category:
                name_lower = pickup.waste_type.name.lower()
                if any(k in name_lower for k in ['plastic', 'paper', 'glass', 'metal', 'cardboard']):
                    pickup.waste_category = 'recyclable'
                elif any(k in name_lower for k in ['electronic', 'e-waste', 'battery', 'circuit']):
                    pickup.waste_category = 'electronic'
                elif any(k in name_lower for k in ['chemical', 'paint', 'oil', 'toxic', 'hazard']):
                    pickup.waste_category = 'hazardous'
                elif any(k in name_lower for k in ['food', 'organic', 'garden', 'compost']):
                    pickup.waste_category = 'organic'
                else:
                    pickup.waste_category = 'non_recyclable'

            pickup.save()

            # Generate QR code
            pickup.generate_qr()
            pickup.save(update_fields=['qr_code'])

            request.user.reward_points += 10
            request.user.save()

            Notification.objects.create(
                user=request.user,
                message=f'Pickup request for {pickup.waste_type.name} submitted! You earned 10 reward points.',
                notif_type='pickup',
                link=f'/pickups/detail/{pickup.id}/'
            )
            messages.success(request, 'Pickup request submitted! You earned 10 reward points.')
            return redirect('user_dashboard')
    else:
        form = PickupRequestForm()
    return render(request, 'pickups/create_pickup.html', {'form': form})


@login_required
def pickup_history(request):
    pickups = PickupRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'pickups/history.html', {'pickups': pickups})


@login_required
def pickup_detail(request, pk):
    pickup = get_object_or_404(PickupRequest, pk=pk, user=request.user)
    all_statuses = ['pending', 'confirmed', 'in_progress', 'completed']
    cancelled = pickup.status == 'cancelled'
    current_index = all_statuses.index(pickup.status) if not cancelled else -1
    timeline = []
    for i, s in enumerate(all_statuses):
        timeline.append({
            'status': s,
            'label': dict(PickupRequest.STATUS_CHOICES).get(s, s),
            'done': i <= current_index and not cancelled,
            'active': i == current_index and not cancelled,
        })
    return render(request, 'pickups/detail.html', {'pickup': pickup, 'timeline': timeline, 'cancelled': cancelled})


@login_required
def cancel_pickup(request, pk):
    pickup = get_object_or_404(PickupRequest, pk=pk, user=request.user)
    if pickup.status == 'pending':
        pickup.status = 'cancelled'
        pickup.save()
        Notification.objects.create(
            user=request.user,
            message=f'Your pickup request for {pickup.waste_type.name} has been cancelled.',
            notif_type='pickup',
            link=f'/pickups/detail/{pickup.id}/'
        )
        messages.success(request, 'Pickup request cancelled.')
    else:
        messages.error(request, 'Only pending pickups can be cancelled.')
    return redirect('user_dashboard')


# ─── Worker Views ────────────────────────────────────────────────────────────

@login_required
def worker_dashboard(request):
    if request.user.user_type != 'worker':
        messages.error(request, 'Access denied.')
        return redirect('home')
    assigned = PickupRequest.objects.filter(
        assigned_worker=request.user
    ).select_related('user', 'waste_type').order_by('-created_at')

    active = list(assigned.filter(status__in=['confirmed', 'in_progress']))
    completed_count = assigned.filter(status='completed').count()
    pending_count = assigned.filter(status='pending').count()

    context = {
        'assigned_pickups': assigned,
        'active_pickups': active,
        'active_count': len(active),
        'completed_count': completed_count,
        'pending_count': pending_count,
        'total_assigned': assigned.count(),
    }
    return render(request, 'workers/dashboard.html', context)


@login_required
def worker_update_status(request, pk, new_status):
    if request.user.user_type != 'worker':
        messages.error(request, 'Access denied.')
        return redirect('home')
    pickup = get_object_or_404(PickupRequest, pk=pk, assigned_worker=request.user)
    allowed = {
        'confirmed': ['in_progress'],
        'in_progress': ['completed'],
    }
    if new_status in allowed.get(pickup.status, []):
        pickup.status = new_status
        pickup.save()
        Notification.objects.create(
            user=pickup.user,
            message=f'Your pickup for {pickup.waste_type.name} is now {pickup.get_status_display()}.',
            notif_type='pickup',
            link=f'/pickups/detail/{pickup.id}/'
        )
        messages.success(request, f'Status updated to {pickup.get_status_display()}.')
    else:
        messages.error(request, 'Invalid status transition.')
    return redirect('worker_dashboard')


# ─── Analytics API ───────────────────────────────────────────────────────────

def analytics_api(request):
    """Returns JSON data for admin charts."""
    from django.db.models import Count
    from django.db.models.functions import TruncDate, TruncMonth
    from django.utils import timezone
    import datetime

    # Daily pickups — last 14 days
    today = timezone.now().date()
    start = today - datetime.timedelta(days=13)
    daily_qs = (
        PickupRequest.objects
        .filter(created_at__date__gte=start)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    daily_map = {str(r['day']): r['count'] for r in daily_qs}
    daily_labels = []
    daily_data = []
    for i in range(14):
        d = start + datetime.timedelta(days=i)
        daily_labels.append(d.strftime('%b %d'))
        daily_data.append(daily_map.get(str(d), 0))

    # Monthly pickups — last 6 months
    month_start = (today.replace(day=1) - datetime.timedelta(days=150)).replace(day=1)
    monthly_qs = (
        PickupRequest.objects
        .filter(created_at__date__gte=month_start)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    monthly_labels = [r['month'].strftime('%b %Y') for r in monthly_qs]
    monthly_data = [r['count'] for r in monthly_qs]

    # Waste category breakdown
    cat_qs = (
        PickupRequest.objects
        .exclude(waste_category='')
        .values('waste_category')
        .annotate(count=Count('id'))
    )
    cat_labels = [r['waste_category'].replace('_', ' ').title() for r in cat_qs]
    cat_data = [r['count'] for r in cat_qs]

    return JsonResponse({
        'daily': {'labels': daily_labels, 'data': daily_data},
        'monthly': {'labels': monthly_labels, 'data': monthly_data},
        'categories': {'labels': cat_labels, 'data': cat_data},
    })
