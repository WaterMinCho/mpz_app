from django.contrib import admin
from .models import Post, PostImage, PostTag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'post_type', 'is_published', 'view_count', 'created_at']
    list_filter = ['post_type', 'is_published']
    search_fields = ['user__username', 'title', 'content']
    list_editable = ['is_published']
    readonly_fields = ['created_at', 'updated_at', 'view_count', 'like_count', 'comment_count']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'title', 'content', 'post_type')
        }),
        ('상태 정보', {
            'fields': ('is_published', 'view_count', 'like_count', 'comment_count')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'image_url', 'sequence', 'caption', 'created_at']
    list_filter = ['post__post_type', 'post__is_published']
    search_fields = ['post__title', 'post__user__username']
    list_editable = ['sequence', 'caption']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['post', 'sequence']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('post', 'image_url', 'sequence', 'caption')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'tag_name', 'created_at']
    list_filter = ['post__post_type']
    search_fields = ['post__title', 'tag_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('post', 'tag_name')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
