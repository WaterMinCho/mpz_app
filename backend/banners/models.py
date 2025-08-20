from django.db import models
from common.models import BaseModel


class Banner(BaseModel):
    """배너 모델"""
    
    TYPE_CHOICES = [
        ('main', '메인'),
        ('sub', '서브'),
    ]
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='main', help_text="배너 타입")
    title = models.CharField(max_length=200, blank=True, null=True, help_text="배너 제목")
    description = models.TextField(blank=True, null=True, help_text="배너 설명")
    alt = models.CharField(max_length=200, help_text="이미지 대체 텍스트")
    image_url = models.CharField(max_length=500, help_text="R2 이미지 URL")
    order_index = models.IntegerField(default=0, help_text="캐러셀 순서")
    is_active = models.BooleanField(default=True, help_text="활성화 상태")
    link_url = models.CharField(max_length=500, blank=True, null=True, help_text="클릭 시 이동할 URL")
    
    class Meta:
        db_table = 'banners'
        verbose_name = '배너'
        verbose_name_plural = '배너들'
        ordering = ['type', 'order_index']
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.title or self.alt}"
