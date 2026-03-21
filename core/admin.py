from django.contrib import admin
from .models import BlogPost, ContactMessage, WasteTip


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'content', 'author']
    readonly_fields = ['created_at']
    fields = ['title', 'author', 'content', 'image', 'created_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    fields = ['name', 'email', 'subject', 'message', 'is_read', 'created_at']


@admin.register(WasteTip)
class WasteTipAdmin(admin.ModelAdmin):
    list_display = ['tip', 'category', 'active']
    list_filter = ['category', 'active']
    search_fields = ['tip']
