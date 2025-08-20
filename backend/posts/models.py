from django.db import models
from django.conf import settings
from common.models import BaseModel


class Post(BaseModel):
    """포스트 모델"""
    
    POST_TYPE_CHOICES = [
        ('adoption_story', '입양 후기'),
        ('foster_story', '임시보호 후기'),
        ('volunteer_story', '봉사 후기'),
        ('animal_info', '동물 정보'),
        ('center_info', '센터 정보'),
        ('general', '일반'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="작성자")
    title = models.CharField(max_length=200, help_text="제목")
    content = models.TextField(help_text="내용")
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='general', help_text="포스트 타입")
    is_published = models.BooleanField(default=True, help_text="공개 여부")
    view_count = models.IntegerField(default=0, help_text="조회수")
    like_count = models.IntegerField(default=0, help_text="좋아요 수")
    comment_count = models.IntegerField(default=0, help_text="댓글 수")
    
    class Meta:
        db_table = 'posts'
        verbose_name = '포스트'
        verbose_name_plural = '포스트들'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class PostImage(BaseModel):
    """포스트 이미지 모델"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, help_text="관련 포스트")
    image_url = models.CharField(max_length=500, help_text="이미지 URL")
    sequence = models.IntegerField(default=0, help_text="이미지 순서")
    caption = models.CharField(max_length=200, blank=True, null=True, help_text="이미지 설명")
    
    class Meta:
        db_table = 'post_images'
        verbose_name = '포스트 이미지'
        verbose_name_plural = '포스트 이미지들'
        ordering = ['post', 'sequence']
    
    def __str__(self):
        return f"{self.post.title} - 이미지 {self.sequence}"


class PostTag(BaseModel):
    """포스트 태그 모델"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, help_text="관련 포스트")
    tag_name = models.CharField(max_length=50, help_text="태그명")
    
    class Meta:
        db_table = 'post_tags'
        verbose_name = '포스트 태그'
        verbose_name_plural = '포스트 태그들'
        unique_together = ['post', 'tag_name']
    
    def __str__(self):
        return f"{self.post.title} - #{self.tag_name}"
