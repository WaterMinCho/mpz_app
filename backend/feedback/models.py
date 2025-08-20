from django.db import models
from django.conf import settings
from common.models import BaseModel


class Feedback(BaseModel):
    """피드백 모델"""
    
    FEEDBACK_TYPE_CHOICES = [
        ('bug', '버그 신고'),
        ('feature', '기능 제안'),
        ('complaint', '불만 사항'),
        ('praise', '칭찬'),
        ('other', '기타'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('in_progress', '처리중'),
        ('resolved', '해결됨'),
        ('rejected', '거부됨'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="피드백 작성자")
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='admin_feedbacks', help_text="처리 담당자")
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES, help_text="피드백 타입")
    title = models.CharField(max_length=200, help_text="제목")
    content = models.TextField(help_text="내용")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', help_text="처리 상태")
    admin_response = models.TextField(blank=True, null=True, help_text="관리자 답변")
    priority = models.IntegerField(default=1, help_text="우선순위 (1-5)")
    
    class Meta:
        db_table = 'feedback'
        verbose_name = '피드백'
        verbose_name_plural = '피드백들'
    
    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.get_status_display()})"


class FeedbackStat(BaseModel):
    """피드백 통계 모델"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="사용자")
    total_feedback = models.IntegerField(default=0, help_text="총 피드백 수")
    resolved_feedback = models.IntegerField(default=0, help_text="해결된 피드백 수")
    pending_feedback = models.IntegerField(default=0, help_text="대기중인 피드백 수")
    average_response_time = models.FloatField(default=0.0, help_text="평균 응답 시간 (시간)")
    
    class Meta:
        db_table = 'feedback_stats'
        verbose_name = '피드백 통계'
        verbose_name_plural = '피드백 통계들'
        unique_together = ['user']
    
    def __str__(self):
        return f"{self.user.username} - 피드백 통계"
