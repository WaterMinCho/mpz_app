from django.contrib import admin
from .models import Animal, AnimalImage


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['name', 'center', 'status', 'age', 'is_female', 'created_at']
    list_filter = ['status', 'is_female', 'neutering', 'center']
    search_fields = ['name', 'center__name', 'breed', 'announce_number']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('center', 'name', 'announce_number', 'breed', 'age', 'is_female', 'weight')
        }),
        ('건강 정보', {
            'fields': ('neutering', 'vaccination', 'heartworm', 'health_notes', 'special_needs')
        }),
        ('상태 및 설명', {
            'fields': ('status', 'description', 'personality', 'is_public')
        }),
        ('입양 관련', {
            'fields': ('adoption_fee',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AnimalImage)
class AnimalImageAdmin(admin.ModelAdmin):
    list_display = ['animal', 'image_url', 'is_primary', 'sequence', 'created_at']
    list_filter = ['is_primary', 'animal__center']
    search_fields = ['animal__name', 'animal__center__name']
    list_editable = ['is_primary', 'sequence']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['animal', 'sequence']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('animal', 'image_url', 'is_primary', 'sequence')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
