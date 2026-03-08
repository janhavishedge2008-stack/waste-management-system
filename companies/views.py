from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CompanyWasteRequest, WasteType
from .forms import CompanyWasteRequestForm

@login_required
def company_dashboard(request):
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    requests = CompanyWasteRequest.objects.filter(company=request.user)
    context = {'requests': requests}
    return render(request, 'companies/dashboard.html', context)

@login_required
def create_waste_request(request):
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    if request.method == 'POST':
        form = CompanyWasteRequestForm(request.POST)
        if form.is_valid():
            waste_request = form.save(commit=False)
            waste_request.company = request.user
            waste_request.save()
            messages.success(request, 'Waste request submitted successfully!')
            return redirect('company_dashboard')
    else:
        form = CompanyWasteRequestForm()
    return render(request, 'companies/create_request.html', {'form': form})

@login_required
def available_waste(request):
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    waste_types = WasteType.objects.all()
    return render(request, 'companies/available_waste.html', {'waste_types': waste_types})

def company_tieup_page(request):
    return render(request, 'companies/tieup.html')
