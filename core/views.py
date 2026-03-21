from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from .models import BlogPost, ContactMessage, WasteTip
from companies.models import WasteType
from pickups.models import PickupRequest
from users.models import User


def home(request):
    total_pickups = PickupRequest.objects.count()
    completed_pickups = PickupRequest.objects.filter(status='completed').count()
    waste_types_count = WasteType.objects.count()
    total_users = User.objects.filter(user_type='regular').count()
    recent_blogs = BlogPost.objects.all()[:3]
    tip = WasteTip.get_tip_of_the_day()

    context = {
        'total_pickups': total_pickups,
        'completed_pickups': completed_pickups,
        'waste_types_count': waste_types_count,
        'total_users': total_users,
        'recent_blogs': recent_blogs,
        'tip': tip,
    }
    return render(request, 'core/home.html', context)


def about(request):
    total_users = User.objects.filter(user_type='regular').count()
    total_companies = User.objects.filter(user_type='company').count()
    total_pickups = PickupRequest.objects.count()
    completed = PickupRequest.objects.filter(status='completed').count()
    context = {
        'total_users': total_users,
        'total_companies': total_companies,
        'total_pickups': total_pickups,
        'completed': completed,
    }
    return render(request, 'core/about.html', context)


def services(request):
    waste_types = WasteType.objects.all()
    return render(request, 'core/services.html', {'waste_types': waste_types})


def how_it_works(request):
    return render(request, 'core/how_it_works.html')


def recycling(request):
    waste_types = WasteType.objects.all()
    return render(request, 'core/recycling.html', {'waste_types': waste_types})


def blog(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__icontains=search_query)
        )
    else:
        posts = BlogPost.objects.all()
    return render(request, 'core/blog.html', {'posts': posts, 'search_query': search_query})


def pricing(request):
    return render(request, 'core/pricing.html')


def faq(request):
    faqs = [
        {'question': 'How do I schedule a pickup?', 'answer': 'Click "Schedule Pickup", fill in your details, select waste type, and choose a date and time.'},
        {'question': 'What types of waste do you accept?', 'answer': f'We accept {WasteType.objects.count()} types of waste including plastic, paper, metal, glass, e-waste, and organic waste.'},
        {'question': 'Is there a fee for pickup service?', 'answer': 'Basic pickup is free for registered users. Premium services are available for businesses and bulk waste.'},
        {'question': 'How do I earn reward points?', 'answer': 'You earn 10 points for every successful pickup request. Points unlock Silver, Gold, and Platinum levels.'},
        {'question': 'Can companies partner with you?', 'answer': 'Yes! Register through our Company Tie-Up page to source recycled materials for your operations.'},
        {'question': 'How do I track my pickup status?', 'answer': 'Visit your dashboard to see real-time status updates for all your pickup requests.'},
        {'question': 'What is the leaderboard?', 'answer': 'The leaderboard ranks users by reward points. Top recyclers earn special recognition and badges.'},
    ]
    return render(request, 'core/faq.html', {'faqs': faqs})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message_text)
        messages.success(request, 'Thank you! We will get back to you soon.')
        return redirect('contact')
    return render(request, 'core/contact.html')
