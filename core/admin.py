from django.contrib import admin
from .models import BlogPost, ContactMessage

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'has_image']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content', 'author']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Blog Content', {
            'fields': ('title', 'author', 'content')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_recent']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def is_recent(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        return obj.created_at >= timezone.now() - timedelta(days=7)
    is_recent.boolean = True
    is_recent.short_description = 'Recent (7 days)'
