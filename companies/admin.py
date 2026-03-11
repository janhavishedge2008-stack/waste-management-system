from django.contrib import admin
from .models import WasteType, CompanyWasteRequest

class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class CompanyWasteRequestAdmin(admin.ModelAdmin):
    list_display = ['get_company_name', 'get_company_email', 'waste_type', 'quantity', 'unit', 'status', 'created_at']
    list_filter = ['status', 'waste_type', 'created_at']
    search_fields = ['company__username', 'company__email', 'company__company_name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'get_company_details']
    
    fields = ['get_company_details', 'company', 'waste_type', 'quantity', 'unit', 
              'description', 'status', 'created_at', 'updated_at']
    
    actions = ['approve_requests', 'fulfill_requests', 'cancel_requests']
    
    def get_company_name(self, obj):
        return obj.company.company_name if obj.company.company_name else obj.company.username
    get_company_name.short_description = 'Company Name'
    get_company_name.admin_order_field = 'company__company_name'
    
    def get_company_email(self, obj):
        return obj.company.email
    get_company_email.short_description = 'Company Email'
    get_company_email.admin_order_field = 'company__email'
    
    def get_company_details(self, obj):
        details = f"""
        <strong>Company:</strong> {obj.company.company_name or obj.company.username}<br>
        <strong>Email:</strong> {obj.company.email}<br>
        <strong>Phone:</strong> {obj.company.phone or 'N/A'}<br>
        <strong>User Type:</strong> {obj.company.user_type}<br>
        <strong>Requested Waste:</strong> {obj.waste_type.name}<br>
        <strong>Quantity:</strong> {obj.quantity} {obj.unit}
        """
        return details
    get_company_details.short_description = 'Company Details'
    get_company_details.allow_tags = True
    
    def approve_requests(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} request(s) approved.')
    approve_requests.short_description = "✓ Approve selected requests"
    
    def fulfill_requests(self, request, queryset):
        updated = queryset.update(status='fulfilled')
        self.message_user(request, f'{updated} request(s) fulfilled.')
    fulfill_requests.short_description = "✓ Mark as fulfilled"
    
    def cancel_requests(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} request(s) cancelled.')
    cancel_requests.short_description = "✗ Cancel selected requests"
    
    def changelist_view(self, request, extra_context=None):
        # Add summary statistics
        extra_context = extra_context or {}
        extra_context['total_requests'] = CompanyWasteRequest.objects.count()
        extra_context['pending_requests'] = CompanyWasteRequest.objects.filter(status='pending').count()
        extra_context['approved_requests'] = CompanyWasteRequest.objects.filter(status='approved').count()
        extra_context['fulfilled_requests'] = CompanyWasteRequest.objects.filter(status='fulfilled').count()
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(WasteType, WasteTypeAdmin)
admin.site.register(CompanyWasteRequest, CompanyWasteRequestAdmin)
