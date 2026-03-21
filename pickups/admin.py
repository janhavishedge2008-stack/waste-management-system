from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count
from django import forms
from .models import PickupRequest
from users.models import User


class PickupRequestAdminForm(forms.ModelForm):
    """Restrict assigned_worker to workers only and assigned_company to companies only."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_worker'].queryset = User.objects.filter(user_type='worker', is_active=True)
        self.fields['assigned_worker'].required = False
        self.fields['assigned_company'].queryset = User.objects.filter(user_type='company', is_active=True)
        self.fields['assigned_company'].required = False

    class Meta:
        model = PickupRequest
        fields = '__all__'


@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    form = PickupRequestAdminForm
    list_display = ['get_user_name', 'get_user_email', 'waste_type', 'location',
                    'pickup_date', 'status_badge', 'timeline_progress', 'assigned_worker_display', 'created_at']
    list_filter  = ['status', 'waste_type', 'pickup_date', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['created_at', 'updated_at', 'status_timeline_widget', 'get_user_details', 'qr_code_display']
    ordering = ['-created_at']

    fields = [
        'status_timeline_widget',
        'get_user_details',
        'user', 'waste_type', 'waste_category', 'location',
        'latitude', 'longitude',
        'pickup_date', 'pickup_time',
        'quantity_estimate', 'special_instructions',
        'waste_image', 'qr_code_display',
        'assigned_company', 'assigned_worker', 'admin_notes',
        'status', 'created_at', 'updated_at',
    ]

    actions = ['mark_confirmed', 'mark_in_progress', 'mark_completed', 'mark_cancelled']

    # ── list display helpers ──────────────────────────────────────────────────

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = 'User'
    get_user_name.admin_order_field = 'user__username'

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'

    def status_badge(self, obj):
        colors = {
            'pending':     ('#ffc107', '#000'),
            'confirmed':   ('#17a2b8', '#fff'),
            'in_progress': ('#fd7e14', '#fff'),
            'completed':   ('#28a745', '#fff'),
            'cancelled':   ('#dc3545', '#fff'),
        }
        icons = {
            'pending': '⏳', 'confirmed': '✅',
            'in_progress': '🚛', 'completed': '🎉', 'cancelled': '❌',
        }
        bg, fg = colors.get(obj.status, ('#6c757d', '#fff'))
        icon   = icons.get(obj.status, '')
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:20px;'
            'font-size:12px;font-weight:600;">{} {}</span>',
            bg, fg, icon, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    def timeline_progress(self, obj):
        steps = ['pending', 'confirmed', 'in_progress', 'completed']
        if obj.status == 'cancelled':
            return format_html(
                '<span style="color:#dc3545;font-size:12px;">❌ Cancelled</span>'
            )
        try:
            idx = steps.index(obj.status)
        except ValueError:
            idx = 0
        pct = int((idx / (len(steps) - 1)) * 100)
        return format_html(
            '<div style="width:100px;background:#e9ecef;border-radius:4px;height:8px;">'
            '<div style="width:{}%;background:linear-gradient(90deg,#28a745,#20c997);'
            'height:8px;border-radius:4px;"></div></div>'
            '<small style="color:#666;font-size:11px;">{}/4</small>',
            pct, idx + 1
        )
    timeline_progress.short_description = 'Progress'

    def assigned_worker_display(self, obj):
        if obj.assigned_worker:
            return format_html(
                '<span style="background:#fd7e14;color:white;padding:2px 8px;border-radius:10px;font-size:11px;">🚛 {}</span>',
                obj.assigned_worker.username
            )
        return format_html('<span style="color:#aaa;font-size:11px;">Unassigned</span>')
    assigned_worker_display.short_description = 'Worker'

    # ── detail page: visual timeline widget ──────────────────────────────────

    def status_timeline_widget(self, obj):
        steps = [
            ('pending',     '⏳', 'Pending',     'Pickup request submitted by user.'),
            ('confirmed',   '✅', 'Confirmed',   'Pickup confirmed. Team will arrive on scheduled date.'),
            ('in_progress', '🚛', 'In Progress', 'Team is on the way / collecting waste.'),
            ('completed',   '🎉', 'Completed',   'Waste collected successfully. Inventory updated.'),
        ]
        cancelled = obj.status == 'cancelled'
        try:
            current_idx = [s[0] for s in steps].index(obj.status)
        except ValueError:
            current_idx = -1

        # Build timeline HTML
        timeline_html = ''
        for i, (status, icon, label, desc) in enumerate(steps):
            if cancelled:
                dot_style = 'background:#e9ecef;border:2px solid #dee2e6;color:#aaa;'
                text_color = '#aaa'
            elif i < current_idx:
                dot_style = 'background:#28a745;border:2px solid #28a745;color:white;'
                text_color = '#28a745'
            elif i == current_idx:
                dot_style = ('background:#28a745;border:3px solid #28a745;color:white;'
                             'box-shadow:0 0 0 4px rgba(40,167,69,0.2);')
                text_color = '#28a745'
            else:
                dot_style = 'background:#f8f9fa;border:2px solid #dee2e6;color:#aaa;'
                text_color = '#999'

            check = '✓' if i < current_idx else icon
            active_label = '<br><small style="color:#28a745;font-weight:600;">▶ Current Status</small>' if i == current_idx and not cancelled else ''

            timeline_html += f'''
            <div style="display:flex;align-items:flex-start;gap:16px;margin-bottom:20px;position:relative;">
                <div style="width:44px;height:44px;border-radius:50%;display:flex;align-items:center;
                            justify-content:center;font-size:1.1rem;flex-shrink:0;{dot_style}">
                    {check}
                </div>
                <div style="flex:1;padding-top:6px;">
                    <div style="font-weight:700;font-size:0.95rem;color:{text_color};">{label}{active_label}</div>
                    <div style="font-size:0.8rem;color:#888;margin-top:2px;">{desc}</div>
                </div>
            </div>
            '''

        # Quick action buttons — use absolute URLs to avoid redirect loops
        pk = obj.pk
        base = f'/admin/pickups/pickuprequest/status/{pk}'
        btn_style = ('display:inline-block;padding:8px 16px;border-radius:8px;'
                     'font-weight:600;font-size:13px;text-decoration:none;margin:4px;')

        buttons = ''
        if not cancelled:
            if obj.status == 'pending':
                buttons += (f'<a href="{base}/confirmed/" style="{btn_style}'
                            f'background:#17a2b8;color:white;">✅ Confirm Pickup</a>')
            if obj.status == 'confirmed':
                buttons += (f'<a href="{base}/in_progress/" style="{btn_style}'
                            f'background:#fd7e14;color:white;">🚛 Mark In Progress</a>')
            if obj.status in ('confirmed', 'in_progress'):
                buttons += (f'<a href="{base}/completed/" style="{btn_style}'
                            f'background:#28a745;color:white;">🎉 Mark Completed</a>')
            if obj.status != 'completed':
                buttons += (f'<a href="{base}/cancelled/" style="{btn_style}'
                            f'background:#dc3545;color:white;" '
                            f'onclick="return confirm(\'Cancel this pickup?\')">❌ Cancel</a>')
        else:
            buttons += (f'<a href="{base}/pending/" style="{btn_style}'
                        f'background:#6c757d;color:white;">↩ Reopen as Pending</a>')

        cancelled_banner = ''
        if cancelled:
            cancelled_banner = '''
            <div style="background:#fee2e2;border:1px solid #fca5a5;border-radius:8px;
                        padding:12px;margin-bottom:16px;color:#991b1b;font-weight:600;">
                ❌ This pickup has been cancelled.
            </div>'''

        return format_html(
            '''<div style="background:#f8f9fa;border-radius:12px;padding:20px;border:1px solid #e9ecef;">
            <h3 style="margin:0 0 20px 0;font-size:1rem;font-weight:700;color:#333;">
                📍 Status Timeline
            </h3>
            {}
            <div style="position:relative;padding-left:22px;border-left:3px solid #e9ecef;">
                {}
            </div>
            <div style="margin-top:20px;padding-top:16px;border-top:1px solid #e9ecef;">
                <div style="font-size:0.8rem;color:#888;margin-bottom:8px;font-weight:600;">
                    QUICK ACTIONS
                </div>
                {}
            </div>
            </div>''',
            format_html(cancelled_banner),
            format_html(timeline_html),
            format_html(buttons),
        )
    status_timeline_widget.short_description = ''

    # ── user details readonly field ───────────────────────────────────────────

    def get_user_details(self, obj):
        return format_html(
            '''<div style="background:#f0fdf4;border-radius:8px;padding:12px;border-left:4px solid #28a745;">
            <strong>👤 User:</strong> {} &nbsp;|&nbsp;
            <strong>📧 Email:</strong> {} &nbsp;|&nbsp;
            <strong>📞 Phone:</strong> {} &nbsp;|&nbsp;
            <strong>🏆 Points:</strong> {}
            </div>''',
            obj.user.get_full_name() or obj.user.username,
            obj.user.email,
            obj.user.phone or 'N/A',
            obj.user.reward_points,
        )
    get_user_details.short_description = 'User Info'

    def qr_code_display(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" style="width:120px;height:120px;border:1px solid #ddd;border-radius:8px;" />',
                obj.qr_code.url
            )
        return format_html('<span style="color:#aaa;">QR code not generated yet.</span>')
    qr_code_display.short_description = 'QR Code'

    # ── custom URL for status transitions ────────────────────────────────────

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                'status/<int:pk>/<str:new_status>/',
                self.admin_site.admin_view(self.change_status_view),
                name='pickup_change_status',
            ),
        ]
        return custom + urls

    def change_status_view(self, request, pk, new_status):
        valid = ['pending', 'confirmed', 'in_progress', 'completed', 'cancelled']
        pickup = get_object_or_404(PickupRequest, pk=pk)

        if new_status not in valid:
            messages.error(request, 'Invalid status.')
            return redirect(f'/admin/pickups/pickuprequest/{pk}/change/')

        pickup.status = new_status
        pickup.save()  # triggers inventory signal on completed

        from users.models import Notification
        status_messages = {
            'confirmed':   f'Your pickup for {pickup.waste_type.name} on {pickup.pickup_date} has been confirmed!',
            'in_progress': f'Our team is on the way to collect your {pickup.waste_type.name}.',
            'completed':   f'Your {pickup.waste_type.name} pickup is complete! Inventory updated.',
            'cancelled':   f'Your pickup for {pickup.waste_type.name} has been cancelled by admin.',
            'pending':     f'Your pickup for {pickup.waste_type.name} has been reopened.',
        }
        if new_status in status_messages:
            Notification.objects.create(
                user=pickup.user,
                message=status_messages[new_status],
                notif_type='pickup',
                link=f'/pickups/detail/{pickup.id}/'
            )

        label = dict(PickupRequest.STATUS_CHOICES).get(new_status, new_status)
        messages.success(
            request,
            f'Pickup #{pk} ({pickup.user.username} — {pickup.waste_type.name}) updated to "{label}".'
        )

        # Redirect back to where the request came from (dashboard or detail page)
        referer = request.META.get('HTTP_REFERER', '')
        if 'admin/' in referer and f'status/{pk}' not in referer:
            return redirect(referer)
        return redirect(f'/admin/pickups/pickuprequest/{pk}/change/')

    # ── bulk actions ──────────────────────────────────────────────────────────

    def mark_confirmed(self, request, queryset):
        n = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'{n} pickup(s) confirmed.')
    mark_confirmed.short_description = '✅ Confirm selected (pending only)'

    def mark_in_progress(self, request, queryset):
        n = queryset.filter(status='confirmed').update(status='in_progress')
        self.message_user(request, f'{n} pickup(s) marked in progress.')
    mark_in_progress.short_description = '🚛 Mark in progress (confirmed only)'

    def mark_completed(self, request, queryset):
        count = 0
        for p in queryset.exclude(status__in=['completed', 'cancelled']):
            p.status = 'completed'
            p.save()  # triggers inventory signal
            count += 1
        self.message_user(request, f'{count} pickup(s) marked completed. Inventory updated.')
    mark_completed.short_description = '🎉 Mark completed & update inventory'

    def mark_cancelled(self, request, queryset):
        n = queryset.exclude(status='completed').update(status='cancelled')
        self.message_user(request, f'{n} pickup(s) cancelled.')
    mark_cancelled.short_description = '❌ Cancel selected'

    # ── changelist stats ──────────────────────────────────────────────────────

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_requests']    = PickupRequest.objects.count()
        extra_context['pending_requests']  = PickupRequest.objects.filter(status='pending').count()
        extra_context['confirmed_requests']= PickupRequest.objects.filter(status='confirmed').count()
        extra_context['in_progress_requests'] = PickupRequest.objects.filter(status='in_progress').count()
        extra_context['completed_requests']= PickupRequest.objects.filter(status='completed').count()
        extra_context['unique_users']      = PickupRequest.objects.values('user').distinct().count()
        extra_context['waste_type_stats']  = (
            PickupRequest.objects.values('waste_type__name')
            .annotate(count=Count('id')).order_by('-count')[:5]
        )
        return super().changelist_view(request, extra_context=extra_context)
