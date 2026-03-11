from django.contrib import admin
from .models import PickupRequest

class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ['get_user_name', 'get_user_email', 'waste_type', 'location', 'pickup_date', 'status', 'created_at']
    list_filter = ['status', 'waste_type', 'pickup_date', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['created_at', 'updated_at', 'get_user_details']
    
    fields = ['get_user_details', 'user', 'waste_type', 'location', 'pickup_date', 
              'pickup_time', 'quantity_estimate', 'special_instructions', 'status', 
              'created_at', 'updated_at']
    
    actions = ['mark_completed', 'mark_in_progress', 'mark_confirmed']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = 'User Name'
    get_user_name.admin_order_field = 'user__username'
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'
    get_user_email.admin_order_field = 'user__email'
    
    def get_user_details(self, obj):
        details = f"""
        <strong>User:</strong> {obj.user.username}<br>
        <strong>Email:</strong> {obj.user.email}<br>
        <strong>Phone:</strong> {obj.user.phone or 'N/A'}<br>
        <strong>Waste Type:</strong> {obj.waste_type.name}<br>
        <strong>Location:</strong> {obj.location}<br>
        <strong>Pickup Date:</strong> {obj.pickup_date}<br>
        <strong>Quantity:</strong> {obj.quantity_estimate or 'Not specified'}
        """
        return details
    get_user_details.short_description = 'User Details'
    get_user_details.allow_tags = True
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} pickup(s) marked as completed.')
    mark_completed.short_description = "✓ Mark as completed"
    
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} pickup(s) marked as in progress.')
    mark_in_progress.short_description = "⏳ Mark as in progress"
    
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} pickup(s) marked as confirmed.')
    mark_confirmed.short_description = "✓ Mark as confirmed"
    
    def changelist_view(self, request, extra_context=None):
        # Add summary statistics
        from django.db.models import Count
        extra_context = extra_context or {}
        
        # Total counts
        extra_context['total_requests'] = PickupRequest.objects.count()
        extra_context['pending_requests'] = PickupRequest.objects.filter(status='pending').count()
        extra_context['confirmed_requests'] = PickupRequest.objects.filter(status='confirmed').count()
        extra_context['in_progress_requests'] = PickupRequest.objects.filter(status='in_progress').count()
        extra_context['completed_requests'] = PickupRequest.objects.filter(status='completed').count()
        
        # Requests by waste type
        waste_type_stats = PickupRequest.objects.values('waste_type__name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        extra_context['waste_type_stats'] = waste_type_stats
        
        # Unique users who sent requests
        extra_context['unique_users'] = PickupRequest.objects.values('user').distinct().count()
        
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(PickupRequest, PickupRequestAdmin)
