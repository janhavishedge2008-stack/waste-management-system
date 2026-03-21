from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import WasteType, CompanyWasteRequest, CollectedWaste


@admin.register(WasteType)
class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'description', 'available_stock']
    search_fields = ['name']

    def available_stock(self, obj):
        try:
            inv = obj.inventory
            color = '#28a745' if inv.available_quantity > 0 else '#dc3545'
            return format_html(
                '<span style="color:{};font-weight:bold;">{} {}</span>',
                color, inv.available_quantity, inv.unit
            )
        except CollectedWaste.DoesNotExist:
            return format_html('<span style="color:#999;">No stock</span>')
    available_stock.short_description = 'Available Stock'


@admin.register(CollectedWaste)
class CollectedWasteAdmin(admin.ModelAdmin):
    list_display = ['waste_type', 'total_collected_display', 'available_display', 'unit', 'last_updated']
    readonly_fields = ['total_quantity', 'available_quantity', 'last_updated', 'inventory_card']
    fields = ['inventory_card', 'waste_type', 'total_quantity', 'available_quantity', 'unit', 'last_updated']
    ordering = ['-available_quantity']

    def total_collected_display(self, obj):
        return format_html('<strong>{} {}</strong>', obj.total_quantity, obj.unit)
    total_collected_display.short_description = 'Total Collected'

    def available_display(self, obj):
        color = '#28a745' if obj.available_quantity > 0 else '#dc3545'
        label = 'In Stock' if obj.available_quantity > 0 else 'Out of Stock'
        pct = int((obj.available_quantity / obj.total_quantity * 100)) if obj.total_quantity > 0 else 0
        return format_html(
            '<span style="color:{};font-weight:bold;">{} {}</span>'
            '<div style="background:#e9ecef;border-radius:4px;height:6px;width:100px;margin-top:3px;">'
            '<div style="background:{};height:6px;border-radius:4px;width:{}%;"></div></div>',
            color, obj.available_quantity, obj.unit, color, pct
        )
    available_display.short_description = 'Available'

    def inventory_card(self, obj):
        pct = int((obj.available_quantity / obj.total_quantity * 100)) if obj.total_quantity > 0 else 0
        return format_html(
            '''<div style="background:#f8f9fa;padding:16px;border-radius:8px;border-left:4px solid #28a745;">
            <h3 style="margin:0 0 8px 0;">{} {}</h3>
            <table style="width:100%;border-collapse:collapse;">
                <tr><td style="padding:4px 0;color:#666;">Total Collected:</td><td style="font-weight:bold;">{} {}</td></tr>
                <tr><td style="padding:4px 0;color:#666;">Available:</td><td style="font-weight:bold;color:#28a745;">{} {}</td></tr>
                <tr><td style="padding:4px 0;color:#666;">Dispatched:</td><td style="font-weight:bold;color:#0d6efd;">{} {}</td></tr>
                <tr><td style="padding:4px 0;color:#666;">Stock Level:</td>
                    <td><div style="background:#e9ecef;border-radius:4px;height:10px;width:200px;">
                    <div style="background:#28a745;height:10px;border-radius:4px;width:{}%;"></div></div>
                    <small style="color:#666;">{}% available</small></td></tr>
            </table></div>''',
            obj.waste_type.icon, obj.waste_type.name,
            obj.total_quantity, obj.unit,
            obj.available_quantity, obj.unit,
            obj.total_quantity - obj.available_quantity, obj.unit,
            pct, pct
        )
    inventory_card.short_description = 'Inventory Summary'

    def has_add_permission(self, request):
        return False  # auto-created by signals

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        total_available = CollectedWaste.objects.aggregate(t=Sum('available_quantity'))['t'] or 0
        total_collected = CollectedWaste.objects.aggregate(t=Sum('total_quantity'))['t'] or 0
        extra_context['total_available'] = total_available
        extra_context['total_collected'] = total_collected
        extra_context['in_stock_count'] = CollectedWaste.objects.filter(available_quantity__gt=0).count()
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(CompanyWasteRequest)
class CompanyWasteRequestAdmin(admin.ModelAdmin):
    list_display = ['get_company_name', 'get_company_email', 'waste_type', 'quantity', 'unit', 'available_stock_display', 'status', 'created_at']
    list_filter = ['status', 'waste_type', 'created_at']
    search_fields = ['company__username', 'company__email', 'description']
    readonly_fields = ['created_at', 'updated_at', 'get_company_details']
    fields = ['get_company_details', 'company', 'waste_type', 'quantity', 'unit',
              'description', 'status', 'created_at', 'updated_at']
    actions = ['approve_requests', 'fulfill_requests', 'cancel_requests']

    def get_company_name(self, obj):
        return obj.company.get_full_name() or obj.company.username
    get_company_name.short_description = 'Company'
    get_company_name.admin_order_field = 'company__username'

    def get_company_email(self, obj):
        return obj.company.email
    get_company_email.short_description = 'Email'

    def available_stock_display(self, obj):
        try:
            inv = obj.waste_type.inventory
            color = '#28a745' if inv.available_quantity >= obj.quantity else '#dc3545'
            label = f'{inv.available_quantity} {inv.unit}'
            return format_html('<span style="color:{};font-weight:bold;">{}</span>', color, label)
        except CollectedWaste.DoesNotExist:
            return format_html('<span style="color:#dc3545;">No stock</span>')
    available_stock_display.short_description = 'Stock Available'

    def get_company_details(self, obj):
        try:
            inv = obj.waste_type.inventory
            stock_info = f'{inv.available_quantity} {inv.unit} available'
            stock_color = '#28a745' if inv.available_quantity >= obj.quantity else '#dc3545'
        except CollectedWaste.DoesNotExist:
            stock_info = 'No stock collected yet'
            stock_color = '#dc3545'

        return format_html(
            '''<div style="background:#f8f9fa;padding:12px;border-radius:8px;">
            <strong>Company:</strong> {}<br>
            <strong>Email:</strong> {}<br>
            <strong>Phone:</strong> {}<br>
            <strong>Requested:</strong> {} {} of {}<br>
            <strong>Stock:</strong> <span style="color:{};font-weight:bold;">{}</span>
            </div>''',
            obj.company.get_full_name() or obj.company.username,
            obj.company.email,
            obj.company.phone or 'N/A',
            obj.quantity, obj.unit, obj.waste_type.name,
            stock_color, stock_info
        )
    get_company_details.short_description = 'Details'

    def approve_requests(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} request(s) approved.')
    approve_requests.short_description = "✓ Approve selected"

    def fulfill_requests(self, request, queryset):
        from decimal import Decimal
        fulfilled = 0
        skipped = 0
        for req in queryset.filter(status='approved'):
            try:
                inv = req.waste_type.inventory
                if inv.available_quantity >= req.quantity:
                    inv.available_quantity -= req.quantity
                    inv.save()
                    req.status = 'fulfilled'
                    req.save()
                    # Notify company
                    from users.models import Notification
                    Notification.objects.create(
                        user=req.company,
                        message=f'Your request for {req.quantity}{req.unit} of {req.waste_type.name} has been fulfilled!',
                        notif_type='company',
                        link='/companies/dashboard/'
                    )
                    fulfilled += 1
                else:
                    skipped += 1
            except CollectedWaste.DoesNotExist:
                skipped += 1
        if fulfilled:
            self.message_user(request, f'{fulfilled} request(s) fulfilled and stock updated.')
        if skipped:
            self.message_user(request, f'{skipped} request(s) skipped — insufficient stock.', level='WARNING')
    fulfill_requests.short_description = "✓ Fulfill & deduct stock"

    def cancel_requests(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} request(s) cancelled.')
    cancel_requests.short_description = "✗ Cancel selected"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_requests'] = CompanyWasteRequest.objects.count()
        extra_context['pending_requests'] = CompanyWasteRequest.objects.filter(status='pending').count()
        extra_context['approved_requests'] = CompanyWasteRequest.objects.filter(status='approved').count()
        extra_context['fulfilled_requests'] = CompanyWasteRequest.objects.filter(status='fulfilled').count()
        return super().changelist_view(request, extra_context=extra_context)
