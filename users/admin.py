from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'phone', 'reward_points', 'is_active', 'created_at']
    list_filter = ['user_type', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'phone', 'company_name', 'address']
    readonly_fields = ['created_at', 'last_login', 'date_joined']
    date_hierarchy = 'created_at'
    
    fieldsets = UserAdmin.fieldsets + (
        ('User Type & Contact', {
            'fields': ('user_type', 'phone', 'address')
        }),
        ('Company Information', {
            'fields': ('company_name',),
            'classes': ('collapse',)
        }),
        ('Rewards', {
            'fields': ('reward_points',)
        }),
        ('Important Dates', {
            'fields': ('created_at', 'last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'email', 'phone', 'address')
        }),
    )
