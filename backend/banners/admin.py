from django.contrib import admin
from banners.models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['type', 'title', 'alt', 'order_index', 'is_active', 'created_at']
    list_filter = ['type', 'is_active']
    search_fields = ['title', 'description', 'alt']
    list_editable = ['order_index', 'is_active']
    ordering = ['type', 'order_index']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('type', 'title', 'description', 'alt')
        }),
        ('이미지 및 링크', {
            'fields': ('image_url', 'link_url')
        }),
        ('표시 설정', {
            'fields': ('order_index', 'is_active')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
