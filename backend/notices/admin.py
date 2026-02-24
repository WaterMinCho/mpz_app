from django.contrib import admin
from notices.models import Notice, SuperadminNotice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'center', 'title', 'notice_type', 'is_published', 'is_pinned', 'view_count', 'created_at']
    list_filter = ['notice_type', 'is_published', 'is_pinned']
    search_fields = ['center__name', 'title', 'content']
    list_editable = ['is_published', 'is_pinned']
    readonly_fields = ['created_at', 'updated_at', 'view_count']
    list_select_related = ['center']
    list_per_page = 25
    autocomplete_fields = ['center']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('center', 'title', 'content', 'notice_type')
        }),
        ('표시 설정', {
            'fields': ('is_published', 'is_pinned', 'view_count')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SuperadminNotice)
class SuperadminNoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'notice_type', 'is_published', 'is_pinned', 'view_count', 'created_at']
    list_filter = ['notice_type', 'is_published', 'is_pinned']
    search_fields = ['title', 'content']
    list_editable = ['is_published', 'is_pinned']
    readonly_fields = ['created_at', 'updated_at', 'view_count']
    list_per_page = 25
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'content', 'notice_type')
        }),
        ('표시 설정', {
            'fields': ('is_published', 'is_pinned', 'view_count')
        }),
        ('대상 설정', {
            'fields': ('target_users',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
