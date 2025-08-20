from django.db import models
from centers.models import Center
from common.models import BaseModel


class Notice(BaseModel):
    """센터별 공지사항 모델"""
    
    NOTICE_TYPE_CHOICES = [
        ('general', '일반'),
        ('important', '중요'),
        ('urgent', '긴급'),
        ('event', '이벤트'),
        ('maintenance', '점검'),
    ]
    
    center = models.ForeignKey(Center, on_delete=models.CASCADE, help_text="관련 센터")
    title = models.CharField(max_length=200, help_text="공지사항 제목")
    content = models.TextField(help_text="공지사항 내용")
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPE_CHOICES, default='general', help_text="공지사항 타입")
    is_published = models.BooleanField(default=True, help_text="공개 여부")
    is_pinned = models.BooleanField(default=False, help_text="상단 고정 여부")
    view_count = models.IntegerField(default=0, help_text="조회수")
    
    class Meta:
        db_table = 'notices'
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항들'
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return f"{self.center.name} - {self.title}"


class SuperadminNotice(BaseModel):
    """최고관리자 공지사항 모델"""
    
    NOTICE_TYPE_CHOICES = [
        ('system', '시스템'),
        ('policy', '정책'),
        ('maintenance', '점검'),
        ('update', '업데이트'),
        ('important', '중요'),
    ]
    
    title = models.CharField(max_length=200, help_text="공지사항 제목")
    content = models.TextField(help_text="공지사항 내용")
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPE_CHOICES, default='system', help_text="공지사항 타입")
    is_published = models.BooleanField(default=True, help_text="공개 여부")
    is_pinned = models.BooleanField(default=False, help_text="상단 고정 여부")
    target_users = models.JSONField(blank=True, null=True, help_text="대상 사용자 타입들")
    view_count = models.IntegerField(default=0, help_text="조회수")
    
    class Meta:
        db_table = 'superadmin_notices'
        verbose_name = '최고관리자 공지사항'
        verbose_name_plural = '최고관리자 공지사항들'
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return f"시스템 - {self.title}"
