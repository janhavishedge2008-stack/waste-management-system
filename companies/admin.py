from django.contrib import admin
from .models import WasteType, CompanyWasteRequest

@admin.register(WasteType)
class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(CompanyWasteRequest)
class CompanyWasteRequestAdmin(admin.ModelAdmin):
    list_display = ['company', 'waste_type', 'quantity', 'unit', 'status', 'created_at']
    list_filter = ['status', 'waste_type', 'created_at']
    search_fields = ['company__username', 'description']
    actions = ['approve_requests']
    
    def approve_requests(self, request, queryset):
        queryset.update(status='approved')
    approve_requests.short_description = "Approve selected requests"
