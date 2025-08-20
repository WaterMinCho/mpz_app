from django.db import models
from django.conf import settings
from centers.models import Center
from animals.models import Animal
from common.models import BaseModel


class CenterFavorite(BaseModel):
    """센터 찜 모델"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="사용자")
    center = models.ForeignKey(Center, on_delete=models.CASCADE, help_text="센터")
    
    class Meta:
        db_table = 'center_favorites'
        verbose_name = '센터 찜'
        verbose_name_plural = '센터 찜들'
        unique_together = ['user', 'center']
    
    def __str__(self):
        return f"{self.user.username} -> {self.center.name}"


class AnimalFavorite(BaseModel):
    """동물 찜 모델"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="사용자")
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, help_text="동물")
    
    class Meta:
        db_table = 'animal_favorites'
        verbose_name = '동물 찜'
        verbose_name_plural = '동물 찜들'
        unique_together = ['user', 'animal']
    
    def __str__(self):
        return f"{self.user.username} -> {self.animal.name}"


class Favorite(BaseModel):
    """통합 찜 모델"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="사용자")
    content_type = models.CharField(max_length=50, help_text="찜한 콘텐츠 타입")
    content_id = models.CharField(max_length=100, help_text="찜한 콘텐츠 ID")
    
    class Meta:
        db_table = 'favorites'
        verbose_name = '찜'
        verbose_name_plural = '찜들'
        unique_together = ['user', 'content_type', 'content_id']
    
    def __str__(self):
        return f"{self.user.username} -> {self.content_type}:{self.content_id}"


class PersonalityTest(BaseModel):
    """성격 테스트 모델"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="사용자")
    test_type = models.CharField(max_length=50, help_text="테스트 타입")
    answers = models.JSONField(help_text="테스트 답변들")
    result = models.JSONField(help_text="테스트 결과")
    completed_at = models.DateTimeField(auto_now_add=True, help_text="완료 시간")
    
    class Meta:
        db_table = 'personality_tests'
        verbose_name = '성격 테스트'
        verbose_name_plural = '성격 테스트들'
    
    def __str__(self):
        return f"{self.user.username} - {self.test_type} ({self.completed_at.strftime('%Y-%m-%d')})"
