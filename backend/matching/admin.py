from django.contrib import admin
from .models import (
    MatchingQuestionnaire, MatchingQuestion, MatchingResponse, 
    MatchingSession, MatchingResult, UserPreference
)


class MatchingQuestionInline(admin.TabularInline):
    model = MatchingQuestion
    extra = 1
    fields = ['sequence', 'question_text', 'question_type', 'options', 'weight', 'category']


class MatchingResponseInline(admin.TabularInline):
    model = MatchingResponse
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MatchingQuestionnaire)
class MatchingQuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    list_per_page = 25
    inlines = [MatchingQuestionInline]
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MatchingQuestion)
class MatchingQuestionAdmin(admin.ModelAdmin):
    list_display = ['questionnaire', 'sequence', 'question_text', 'question_type', 'weight', 'category']
    list_filter = ['question_type', 'category']
    search_fields = ['question_text', 'questionnaire__title']
    list_editable = ['sequence', 'weight']
    ordering = ['questionnaire', 'sequence']
    list_select_related = ['questionnaire']
    list_per_page = 25
    autocomplete_fields = ['questionnaire']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('questionnaire', 'sequence', 'question_text', 'question_type')
        }),
        ('옵션 및 가중치', {
            'fields': ('options', 'weight', 'category')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MatchingResponse)
class MatchingResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'questionnaire', 'question', 'selected_options', 'created_at']
    list_filter = ['user__user_type']
    search_fields = ['user__username', 'question__question_text']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['user', 'questionnaire', 'question']
    list_per_page = 25
    autocomplete_fields = ['user', 'questionnaire', 'question']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'questionnaire', 'question', 'selected_options')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MatchingSession)
class MatchingSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'questionnaire', 'is_completed', 'completed_at', 'created_at']
    list_filter = ['is_completed', 'user__user_type']
    search_fields = ['user__username', 'questionnaire__title']
    list_editable = ['is_completed']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['user', 'questionnaire']
    list_per_page = 25
    autocomplete_fields = ['user', 'questionnaire']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'questionnaire', 'is_completed')
        }),
        ('완료 정보', {
            'fields': ('completed_at',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MatchingResult)
class MatchingResultAdmin(admin.ModelAdmin):
    list_display = ['session', 'animal', 'match_score', 'recommendation_level', 'created_at']
    list_filter = ['recommendation_level', 'animal__center__region']
    search_fields = ['session__user__username', 'animal__name', 'animal__center__name']
    list_editable = ['recommendation_level']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['session', 'session__user', 'animal', 'animal__center']
    list_per_page = 25
    autocomplete_fields = ['session', 'animal']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('session', 'animal', 'match_score', 'recommendation_level')
        }),
        ('매칭 결과', {
            'fields': ('compatibility_report', 'matching_factors')
        }),
        ('추가 정보', {
            'fields': ('potential_challenges', 'recommendations'),
            'classes': ('collapse',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'session', 'animal_type', 'size_preference', 'activity_level', 'created_at']
    list_filter = ['animal_type', 'size_preference', 'activity_level', 'user__user_type']
    search_fields = ['user__username', 'session__questionnaire__title']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['user', 'session', 'session__questionnaire']
    list_per_page = 25
    autocomplete_fields = ['user', 'session']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'session')
        }),
        ('선호도 설정', {
            'fields': ('preferences', 'animal_type', 'size_preference', 'activity_level', 'experience_level')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
