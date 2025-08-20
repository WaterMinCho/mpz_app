from django.contrib import admin
from centers.models import Center, AdoptionContractTemplate, QuestionForm


@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'region', 'verified', 'is_public', 'created_at']
    list_filter = ['region', 'verified', 'is_public', 'has_monitoring']
    search_fields = ['name', 'owner__username', 'center_number']
    list_editable = ['verified', 'is_public']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('owner', 'name', 'center_number', 'description', 'image_url')
        }),
        ('위치 정보', {
            'fields': ('location', 'region', 'phone_number')
        }),
        ('입양 관련', {
            'fields': ('adoption_procedure', 'adoption_guidelines', 'adoption_price')
        }),
        ('모니터링', {
            'fields': ('has_monitoring', 'monitoring_period_months', 'monitoring_interval_days', 'monitoring_description')
        }),
        ('상태', {
            'fields': ('verified', 'is_public')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AdoptionContractTemplate)
class AdoptionContractTemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'center', 'is_active', 'created_at']
    list_filter = ['is_active', 'center']
    search_fields = ['title', 'center__name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('center', 'title', 'description', 'is_active')
        }),
        ('계약서 내용', {
            'fields': ('content',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(QuestionForm)
class QuestionFormAdmin(admin.ModelAdmin):
    list_display = ['center', 'question', 'question_type', 'is_required', 'sequence', 'created_at']
    list_filter = ['center', 'question_type', 'is_required']
    search_fields = ['center__name', 'question']
    list_editable = ['is_required', 'sequence']
    ordering = ['center', 'sequence']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('center', 'question', 'question_type', 'is_required', 'sequence')
        }),
        ('선택지', {
            'fields': ('options',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
