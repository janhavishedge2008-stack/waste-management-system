from django.contrib import admin
from .models import PickupRequest

@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'waste_type', 'location', 'pickup_date', 'status', 'created_at']
    list_filter = ['status', 'waste_type', 'pickup_date']
    search_fields = ['user__username', 'user__email', 'location', 'special_instructions']
    date_hierarchy = 'pickup_date'
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['mark_completed', 'mark_in_progress', 'mark_confirmed']
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} pickup(s) marked as completed.')
    mark_completed.short_description = "Mark as completed"
    
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} pickup(s) marked as in progress.')
    mark_in_progress.short_description = "Mark as in progress"
    
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} pickup(s) marked as confirmed.')
    mark_confirmed.short_description = "Mark as confirmed"
