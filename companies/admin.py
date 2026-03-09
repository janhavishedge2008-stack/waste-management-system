from django.contrib import admin
from .models import WasteType, CompanyWasteRequest

class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class CompanyWasteRequestAdmin(admin.ModelAdmin):
    list_display = ['company', 'waste_type', 'quantity', 'unit', 'status', 'created_at']
    list_filter = ['status', 'waste_type']
    search_fields = ['company__username', 'company__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fields = ['company', 'waste_type', 'quantity', 'unit', 'description', 
              'status', 'created_at', 'updated_at']
    
    actions = ['approve_requests', 'fulfill_requests', 'cancel_requests']
    
    def approve_requests(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} request(s) approved.')
    approve_requests.short_description = "Approve selected requests"
    
    def fulfill_requests(self, request, queryset):
        updated = queryset.update(status='fulfilled')
        self.message_user(request, f'{updated} request(s) fulfilled.')
    fulfill_requests.short_description = "Mark as fulfilled"
    
    def cancel_requests(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} request(s) cancelled.')
    cancel_requests.short_description = "Cancel selected requests"

admin.site.register(WasteType, WasteTypeAdmin)
admin.site.register(CompanyWasteRequest, CompanyWasteRequestAdmin)
