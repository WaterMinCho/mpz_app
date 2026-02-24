from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Animal, AnimalImage, AnimalMegaphone, AdoptionApplication


class AnimalImageInline(admin.TabularInline):
    """동물 이미지 인라인"""
    model = AnimalImage
    extra = 1
    fields = ('image_url', 'is_primary', 'sequence', 'image_url_preview')
    readonly_fields = ('image_url_preview',)
    
    def image_url_preview(self, obj):
        if obj.image_url:
            return mark_safe(f'<img src="{obj.image_url}" style="max-height: 50px; max-width: 50px;" />')
        return "이미지 없음"
    image_url_preview.short_description = '미리보기'


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'center', 'age', 'weight', 'is_female_display', 
        'protection_status', 'adoption_status', 'is_public_data',
        'admission_date', 'created_at'
    ]
    list_filter = [
        'protection_status', 'adoption_status', 'is_female', 'is_public_data',
        'center__region', 'admission_date', 'created_at'
    ]
    search_fields = ['name', 'announce_number', 'public_notice_number', 'breed', 'center__name']
    list_per_page = 25
    list_select_related = ['center']
    autocomplete_fields = ['center']
    inlines = [AnimalImageInline]

    autocomplete_fields = ['center']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'center', 'announce_number', 'breed', 'age', 
                      'is_female', 'weight', 'admission_date', 'found_location')
        }),
        ('상태 정보', {
            'fields': ('protection_status', 'adoption_status', 'is_public', 
                      'is_public_data', 'public_notice_number')
        }),
        ('건강/관리', {
            'fields': ('neutering', 'vaccination', 'heartworm', 'adoption_fee')
        }),
        ('설명 및 성격', {
            'fields': ('description', 'personality', 'health_notes', 'special_needs')
        }),
        ('공공데이터', {
            'fields': ('comment', 'notice_start_date', 'notice_end_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'megaphone_count')
    
    def is_female_display(self, obj):
        if obj.is_female:
            return format_html('<span style="color: pink;">♀ 암컷</span>')
        return format_html('<span style="color: blue;">♂ 수컷</span>')
    is_female_display.short_description = '성별'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('center')


@admin.register(AnimalImage)
class AnimalImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'animal', 'image_url_preview', 'is_primary', 'sequence', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['animal__name', 'animal__center__name']
    list_select_related = ['animal']
    list_per_page = 25
    autocomplete_fields = ['animal']
    ordering = ['animal', 'sequence']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('animal', 'image_url', 'is_primary', 'sequence')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_url_preview(self, obj):
        if obj.image_url:
            return mark_safe(f'<img src="{obj.image_url}" style="max-height: 40px; max-width: 40px;" />')
        return "이미지 없음"
    image_url_preview.short_description = '미리보기'


@admin.register(AnimalMegaphone)
class AnimalMegaphoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'animal', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'animal__name', 'animal__center__name']
    list_select_related = ['user', 'animal']
    list_per_page = 25
    autocomplete_fields = ['user', 'animal']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'animal')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'user_link', 'animal_link', 'status_display', 'application_date',
        'approval_date', 'processing_days', 'contact_phone', 'is_active'
    ]
    list_filter = [
        'status', 'application_date', 'approval_date', 'has_pet_experience',
        'can_visit_center'
    ]
    search_fields = [
        'user__username', 'user__email', 'user__phone_number', 
        'animal__name', 'reason', 'contact_phone', 'contact_email'
    ]
    list_per_page = 20
    list_select_related = ['user', 'animal', 'animal__center', 'processed_by']
    autocomplete_fields = ['user', 'animal', 'processed_by']
    
    fieldsets = (
        ('신청자 정보', {
            'fields': ('user', 'contact_phone', 'contact_email', 'home_address', 
                      'family_size', 'has_pet_experience', 'can_visit_center')
        }),
        ('입양 대상', {
            'fields': ('animal',)
        }),
        ('신청 내용', {
            'fields': ('reason', 'status', 'application_date', 'approval_date')
        }),
        ('관리자 정보', {
            'fields': ('processed_by', 'admin_notes'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('application_date',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != 'pending':
            return self.readonly_fields + ('user', 'animal', 'reason', 'contact_phone', 
                                         'contact_email', 'home_address')
        return self.readonly_fields
    
    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:user_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"
    user_link.short_description = '신청자'
    
    def animal_link(self, obj):
        if obj.animal:
            url = reverse('admin:animals_animal_change', args=[obj.animal.id])
            return format_html('<a href="{}">{}</a>', url, obj.animal.name)
        return "-"
    animal_link.short_description = '동물'
    
    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'approved': 'green', 
            'rejected': 'red',
            'cancelled': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', 
                          color, obj.get_status_display())
    status_display.short_description = '상태'
    
    def processing_days(self, obj):
        return obj.processing_days
    processing_days.short_description = '경과일'
    
    def is_active(self, obj):
        return obj.is_active
    is_active.boolean = True
    is_active.short_description = '활성'
    
    def save_model(self, request, obj, form, change):
        if not obj.processed_by:
            obj.processed_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'animal', 'animal__center', 'processed_by')
