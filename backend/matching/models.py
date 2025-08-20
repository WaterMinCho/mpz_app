from django.db import models
from django.conf import settings
from common.models import BaseModel


class MatchingQuestionnaire(BaseModel):
    """매칭 질문지 모델"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="사용자")
    title = models.CharField(max_length=200, help_text="질문지 제목")
    description = models.TextField(blank=True, null=True, help_text="질문지 설명")
    is_active = models.BooleanField(default=True, help_text="활성화 여부")
    completed_at = models.DateTimeField(blank=True, null=True, help_text="완료 시간")
    
    class Meta:
        db_table = 'matching_questionnaires'
        verbose_name = '매칭 질문지'
        verbose_name_plural = '매칭 질문지들'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class MatchingQuestion(BaseModel):
    """매칭 질문 모델"""
    
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', '객관식'),
        ('scale', '척도'),
        ('text', '주관식'),
        ('boolean', '예/아니오'),
    ]
    
    questionnaire = models.ForeignKey(MatchingQuestionnaire, on_delete=models.CASCADE, help_text="관련 질문지")
    question_text = models.TextField(help_text="질문 내용")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, help_text="질문 타입")
    options = models.JSONField(blank=True, null=True, help_text="선택지 옵션들")
    weight = models.FloatField(default=1.0, help_text="질문 가중치")
    sequence = models.IntegerField(default=0, help_text="질문 순서")
    
    class Meta:
        db_table = 'matching_questions'
        verbose_name = '매칭 질문'
        verbose_name_plural = '매칭 질문들'
        ordering = ['questionnaire', 'sequence']
    
    def __str__(self):
        return f"{self.questionnaire.title} - {self.question_text[:50]}"


class MatchingResponse(BaseModel):
    """매칭 질문 응답 모델"""
    
    questionnaire = models.ForeignKey(MatchingQuestionnaire, on_delete=models.CASCADE, help_text="관련 질문지")
    question = models.ForeignKey(MatchingQuestion, on_delete=models.CASCADE, help_text="관련 질문")
    response_value = models.TextField(help_text="응답 값")
    response_score = models.FloatField(blank=True, null=True, help_text="응답 점수")
    
    class Meta:
        db_table = 'matching_responses'
        verbose_name = '매칭 응답'
        verbose_name_plural = '매칭 응답들'
        unique_together = ['questionnaire', 'question']
    
    def __str__(self):
        return f"{self.questionnaire.user.username} - {self.question.question_text[:30]}"


class MatchingSession(BaseModel):
    """매칭 세션 모델"""
    
    SESSION_STATUS_CHOICES = [
        ('active', '활성'),
        ('completed', '완료'),
        ('expired', '만료'),
        ('cancelled', '취소됨'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="사용자")
    questionnaire = models.ForeignKey(MatchingQuestionnaire, on_delete=models.CASCADE, help_text="사용된 질문지")
    session_status = models.CharField(max_length=20, choices=SESSION_STATUS_CHOICES, default='active', help_text="세션 상태")
    started_at = models.DateTimeField(auto_now_add=True, help_text="시작 시간")
    completed_at = models.DateTimeField(blank=True, null=True, help_text="완료 시간")
    expires_at = models.DateTimeField(help_text="만료 시간")
    
    class Meta:
        db_table = 'matching_sessions'
        verbose_name = '매칭 세션'
        verbose_name_plural = '매칭 세션들'
    
    def __str__(self):
        return f"{self.user.username} - {self.session_status}"


class MatchingResult(BaseModel):
    """매칭 결과 모델"""
    
    session = models.ForeignKey(MatchingSession, on_delete=models.CASCADE, help_text="관련 매칭 세션")
    animal_id = models.CharField(max_length=100, help_text="매칭된 동물 ID")
    match_score = models.FloatField(help_text="매칭 점수")
    compatibility_factors = models.JSONField(help_text="호환성 요인들")
    recommendations = models.JSONField(blank=True, null=True, help_text="추천 사항")
    
    class Meta:
        db_table = 'matching_results'
        verbose_name = '매칭 결과'
        verbose_name_plural = '매칭 결과들'
        ordering = ['-match_score']
    
    def __str__(self):
        return f"{self.session.user.username} - 동물 {self.animal_id} (점수: {self.match_score})"


class UserPreference(BaseModel):
    """사용자 선호도 모델"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="사용자")
    preference_type = models.CharField(max_length=50, help_text="선호도 타입")
    preference_value = models.JSONField(help_text="선호도 값")
    weight = models.FloatField(default=1.0, help_text="선호도 가중치")
    is_active = models.BooleanField(default=True, help_text="활성화 여부")
    
    class Meta:
        db_table = 'user_preferences'
        verbose_name = '사용자 선호도'
        verbose_name_plural = '사용자 선호도들'
        unique_together = ['user', 'preference_type']
    
    def __str__(self):
        return f"{self.user.username} - {self.preference_type}"
