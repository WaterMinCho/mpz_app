from django.contrib import admin
from .models import Feedback, FeedbackStat


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'feedback_type', 'title', 'status', 'priority', 'created_at']
    list_filter = ['feedback_type', 'status', 'priority']
    search_fields = ['user__username', 'title', 'content']
    list_editable = ['status', 'priority']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'feedback_type', 'title', 'content')
        }),
        ('처리 정보', {
            'fields': ('status', 'priority', 'admin', 'admin_response')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FeedbackStat)
class FeedbackStatAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_feedback', 'resolved_feedback', 'pending_feedback', 'average_response_time']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('통계 정보', {
            'fields': ('user', 'total_feedback', 'resolved_feedback', 'pending_feedback', 'average_response_time')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
