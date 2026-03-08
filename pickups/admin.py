from django.contrib import admin
from .models import PickupRequest

@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'waste_type', 'location', 'pickup_date', 'status', 'created_at']
    list_filter = ['status', 'waste_type', 'pickup_date']
    search_fields = ['user__username', 'location']
    actions = ['mark_completed', 'mark_in_progress']
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_completed.short_description = "Mark as completed"
    
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_in_progress.short_description = "Mark as in progress"
