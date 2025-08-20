from django.contrib import admin
from .models import Comment, Reply


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'is_edited', 'created_at']
    list_filter = ['is_edited']
    search_fields = ['user__username', 'content']
    list_editable = ['is_edited']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'content', 'is_edited')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'comment', 'content', 'is_edited', 'created_at']
    list_filter = ['is_edited']
    search_fields = ['user__username', 'comment__content', 'content']
    list_editable = ['is_edited']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'comment', 'content', 'is_edited')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
