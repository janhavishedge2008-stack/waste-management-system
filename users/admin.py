from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html
from .models import User, Notification, RegularUser, CompanyUser, WorkerUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'user_type', 'phone')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'


class RegularUserFilter(admin.SimpleListFilter):
    title = 'account type'
    parameter_name = 'account_type'

    def lookups(self, request, model_admin):
        return (
            ('regular', 'Regular Users'),
            ('company', 'Company Users'),
            ('admin', 'Admin Users'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_type=self.value())
        return queryset


# --- Regular Users Admin ---
class RegularUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm

    list_display = ['username', 'email', 'phone', 'address_short', 'reward_points', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['username', 'email', 'phone']
    readonly_fields = ['created_at', 'reward_points', 'user_badge']
    ordering = ['-created_at']

    fieldsets = (
        ('Account Info', {'fields': ('user_badge', 'username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'address')}),
        ('Stats', {'fields': ('reward_points', 'created_at')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user_type='regular')

    def address_short(self, obj):
        return (obj.address[:40] + '...') if obj.address and len(obj.address) > 40 else (obj.address or '—')
    address_short.short_description = 'Address'

    def user_badge(self, obj):
        return format_html(
            '<span style="background:#198754;color:white;padding:4px 12px;border-radius:20px;font-weight:bold;">👤 Regular User</span>'
        )
    user_badge.short_description = 'Type'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        qs = self.get_queryset(request)
        extra_context['total_users'] = qs.count()
        extra_context['active_users'] = qs.filter(is_active=True).count()
        extra_context['inactive_users'] = qs.filter(is_active=False).count()
        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return False  # Users register themselves


# --- Company Users Admin ---
class CompanyUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm

    list_display = ['company_display', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['username', 'email', 'phone']
    readonly_fields = ['created_at', 'company_badge']
    ordering = ['-created_at']

    fieldsets = (
        ('Account Info', {'fields': ('company_badge', 'username', 'email', 'password')}),
        ('Contact Info', {'fields': ('first_name', 'last_name', 'phone', 'address')}),
        ('Stats', {'fields': ('reward_points', 'created_at')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user_type='company')

    def company_display(self, obj):
        name = obj.get_full_name() or obj.username
        return format_html('<strong>{}</strong>', name)
    company_display.short_description = 'Company / Username'
    company_display.admin_order_field = 'username'

    def company_badge(self, obj):
        return format_html(
            '<span style="background:#0d6efd;color:white;padding:4px 12px;border-radius:20px;font-weight:bold;">🏢 Company User</span>'
        )
    company_badge.short_description = 'Type'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        qs = self.get_queryset(request)
        extra_context['total_companies'] = qs.count()
        extra_context['active_companies'] = qs.filter(is_active=True).count()
        extra_context['inactive_companies'] = qs.filter(is_active=False).count()
        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return False  # Companies register themselves


# --- Worker Users Admin ---
class WorkerUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ['username', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['username', 'email', 'phone']
    readonly_fields = ['created_at', 'worker_badge']
    ordering = ['-created_at']

    fieldsets = (
        ('Account Info', {'fields': ('worker_badge', 'username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_active',)}),
        ('Dates', {'fields': ('created_at',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(user_type='worker')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_type = 'worker'
        super().save_model(request, obj, form, change)

    def worker_badge(self, obj):
        return format_html(
            '<span style="background:#fd7e14;color:white;padding:4px 12px;border-radius:20px;font-weight:bold;">🚛 Worker/Collector</span>'
        )
    worker_badge.short_description = 'Type'


# Full user admin (for superuser management)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ['username', 'email', 'user_type_badge', 'phone', 'is_active', 'created_at']
    list_filter = [RegularUserFilter, 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'phone']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Additional Info', {'fields': ('user_type', 'phone', 'address', 'reward_points')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'phone', 'password1', 'password2'),
        }),
    )

    def user_type_badge(self, obj):
        colors = {'regular': '#198754', 'company': '#0d6efd', 'admin': '#dc3545', 'worker': '#fd7e14'}
        icons = {'regular': '👤', 'company': '🏢', 'admin': '🔑', 'worker': '🚛'}
        color = colors.get(obj.user_type, '#6c757d')
        icon = icons.get(obj.user_type, '?')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:12px;">{} {}</span>',
            color, icon, obj.get_user_type_display()
        )
    user_type_badge.short_description = 'User Type'
    user_type_badge.admin_order_field = 'user_type'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_users'] = User.objects.filter(user_type='regular').count()
        extra_context['total_companies'] = User.objects.filter(user_type='company').count()
        extra_context['total_all'] = User.objects.count()
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(User, CustomUserAdmin)
admin.site.register(RegularUser, RegularUserAdmin)
admin.site.register(CompanyUser, CompanyUserAdmin)
admin.site.register(WorkerUser, WorkerUserAdmin)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'notif_type', 'is_read', 'created_at']
    list_filter = ['notif_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'message']
