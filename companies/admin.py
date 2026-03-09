from django.contrib import admin
from .models import WasteType, CompanyWasteRequest

@admin.register(WasteType)
class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(CompanyWasteRequest)
class CompanyWasteRequestAdmin(admin.ModelAdmin):
    list_display = ['company', 'company_email', 'waste_type', 'quantity', 'unit', 'status', 'created_at']
    list_filter = ['status', 'waste_type', 'created_at', 'updated_at']
    search_fields = ['company__username', 'company__email', 'company__company_name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    actions = ['approve_requests', 'fulfill_requests', 'cancel_requests']
    
    fieldsets = (
        ('Company Information', {
            'fields': ('company',)
        }),
        ('Waste Request Details', {
            'fields': ('waste_type', 'quantity', 'unit', 'description')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def company_email(self, obj):
        return obj.company.email
    company_email.short_description = 'Company Email'
    
    def approve_requests(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} request(s) approved successfully.')
    approve_requests.short_description = "Approve selected requests"
    
    def fulfill_requests(self, request, queryset):
        updated = queryset.update(status='fulfilled')
        self.message_user(request, f'{updated} request(s) marked as fulfilled.')
    fulfill_requests.short_description = "Mark as fulfilled"
    
    def cancel_requests(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} request(s) cancelled.')
    cancel_requests.short_description = "Cancel selected requests"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('company', 'waste_type')
