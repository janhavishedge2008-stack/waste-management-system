from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BlogPost, ContactMessage

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def services(request):
    return render(request, 'core/services.html')

def how_it_works(request):
    return render(request, 'core/how_it_works.html')

def recycling(request):
    return render(request, 'core/recycling.html')

def blog(request):
    posts = BlogPost.objects.all()
    return render(request, 'core/blog.html', {'posts': posts})

def pricing(request):
    return render(request, 'core/pricing.html')

def faq(request):
    return render(request, 'core/faq.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, 'Message sent successfully!')
        return redirect('contact')
    return render(request, 'core/contact.html')
