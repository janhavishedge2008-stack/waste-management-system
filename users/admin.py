from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'phone', 'reward_points', 'is_active']
    list_filter = ['user_type', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'phone', 'company_name', 'address']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone', 'address', 'company_name', 'reward_points', 'created_at')
        }),
    )
    
    readonly_fields = ['created_at']
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'email', 'phone', 'address')
        }),
    )
