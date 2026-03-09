from django.contrib import admin
from .models import PickupRequest

@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_email', 'waste_type', 'quantity', 'pickup_date', 'status', 'created_at']
    list_filter = ['status', 'waste_type', 'pickup_date', 'created_at']
    search_fields = ['user__username', 'user__email', 'location', 'address', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'pickup_date'
    actions = ['mark_completed', 'mark_in_progress', 'mark_scheduled']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Pickup Details', {
            'fields': ('waste_type', 'quantity', 'unit', 'pickup_date', 'location', 'address', 'description')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} pickup(s) marked as completed.')
    mark_completed.short_description = "Mark as completed"
    
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} pickup(s) marked as in progress.')
    mark_in_progress.short_description = "Mark as in progress"
    
    def mark_scheduled(self, request, queryset):
        updated = queryset.update(status='scheduled')
        self.message_user(request, f'{updated} pickup(s) marked as scheduled.')
    mark_scheduled.short_description = "Mark as scheduled"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'waste_type')
