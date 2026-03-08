from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PickupRequest
from .forms import PickupRequestForm

@login_required
def create_pickup(request):
    if request.method == 'POST':
        form = PickupRequestForm(request.POST)
        if form.is_valid():
            pickup = form.save(commit=False)
            pickup.user = request.user
            pickup.save()
            request.user.reward_points += 10
            request.user.save()
            messages.success(request, 'Pickup request submitted! You earned 10 reward points.')
            return redirect('user_dashboard')
    else:
        form = PickupRequestForm()
    return render(request, 'pickups/create_pickup.html', {'form': form})

@login_required
def pickup_history(request):
    pickups = PickupRequest.objects.filter(user=request.user)
    return render(request, 'pickups/history.html', {'pickups': pickups})

@login_required
def pickup_detail(request, pk):
    pickup = get_object_or_404(PickupRequest, pk=pk, user=request.user)
    return render(request, 'pickups/detail.html', {'pickup': pickup})

@login_required
def cancel_pickup(request, pk):
    pickup = get_object_or_404(PickupRequest, pk=pk, user=request.user)
    if pickup.status == 'pending':
        pickup.status = 'cancelled'
        pickup.save()
        messages.success(request, 'Pickup request cancelled')
    else:
        messages.error(request, 'Cannot cancel this pickup')
    return redirect('user_dashboard')
