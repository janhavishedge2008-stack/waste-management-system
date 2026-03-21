from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "EcoWaste Management System"
admin.site.site_title = "EcoWaste Admin"
admin.site.index_title = "Live Dashboard"

# Inject live stats into admin index
_original_index = admin.site.__class__.index

def custom_index(self, request, extra_context=None):
    from users.models import User
    from pickups.models import PickupRequest
    from companies.models import WasteType, CompanyWasteRequest, CollectedWaste
    from core.models import ContactMessage
    from django.db.models import Sum

    total_pickups = PickupRequest.objects.count()
    extra_context = extra_context or {}
    extra_context.update({
        'total_regular_users':  User.objects.filter(user_type='regular').count(),
        'total_company_users':  User.objects.filter(user_type='company').count(),
        'total_worker_users':   User.objects.filter(user_type='worker').count(),
        'total_pickups':        total_pickups,
        'pending_pickups':      PickupRequest.objects.filter(status='pending').count(),
        'completed_pickups':    PickupRequest.objects.filter(status='completed').count(),
        'total_waste_requests': CompanyWasteRequest.objects.count(),
        'unread_messages':      ContactMessage.objects.filter(is_read=False).count(),
        'waste_types_count':    WasteType.objects.count(),
        'recent_users':         User.objects.filter(user_type='regular').order_by('-created_at')[:8],
        'recent_companies':     User.objects.filter(user_type='company').order_by('-created_at')[:5],
        'recent_pickups':       PickupRequest.objects.select_related('user', 'waste_type').order_by('-created_at')[:8],
        'waste_inventory':      CollectedWaste.objects.select_related('waste_type').order_by('-available_quantity'),
        'total_available_kg':   CollectedWaste.objects.aggregate(t=Sum('available_quantity'))['t'] or 0,
        'pickup_breakdown': [
            ('Pending',     PickupRequest.objects.filter(status='pending').count(),     '#ffc107', 'pending'),
            ('Confirmed',   PickupRequest.objects.filter(status='confirmed').count(),   '#17a2b8', 'confirmed'),
            ('In Progress', PickupRequest.objects.filter(status='in_progress').count(), '#fd7e14', 'in_progress'),
            ('Completed',   PickupRequest.objects.filter(status='completed').count(),   '#28a745', 'completed'),
            ('Cancelled',   PickupRequest.objects.filter(status='cancelled').count(),   '#dc3545', 'cancelled'),
        ],
    })
    return _original_index(self, request, extra_context)

admin.site.__class__.index = custom_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('companies/', include('companies.urls')),
    path('pickups/', include('pickups.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
