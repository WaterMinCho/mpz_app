from django.db import models
from django.core.files.storage import default_storage
from django.conf import settings
import uuid
import os
from datetime import datetime
from common.models import BaseModel


def banner_upload_path(instance, filename):
    """배너 파일 업로드 경로 생성 (timestamp 기반 안전한 파일명)"""
    # 파일 확장자 추출
    ext = os.path.splitext(filename)[1].lower()
    if not ext:
        ext = '.jpg'  # 기본값
    
    # timestamp 기반 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]  # 밀리초까지
    safe_filename = f"banner_{timestamp}{ext}"
    
    return f"banners/{safe_filename}"


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
    image_file = models.ImageField(upload_to=banner_upload_path, blank=True, null=True, help_text="배너 이미지 파일")
    image_url = models.CharField(max_length=500, blank=True, null=True, help_text="이미지 URL (파일 업로드 시 자동 생성)")
    order_index = models.IntegerField(default=0, help_text="캐러셀 순서")
    is_active = models.BooleanField(default=True, help_text="활성화 상태")
    link_url = models.CharField(max_length=500, blank=True, null=True, help_text="클릭 시 이동할 URL")
    
    class Meta:
        db_table = 'banners'
        verbose_name = '배너'
        verbose_name_plural = '배너들'
        ordering = ['type', 'order_index']
    
    def save(self, *args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)

        if self.image_file and hasattr(self.image_file, 'file'):
            try:
                from storage_service.services import StorageClient
                import mimetypes

                storage = StorageClient()

                file_extension = os.path.splitext(self.image_file.name)[1]
                if not file_extension:
                    file_extension = '.jpg'

                content_type = mimetypes.guess_type(self.image_file.name)[0] or 'image/jpeg'
                key = f"banners/{uuid.uuid4()}{file_extension}"

                self.image_file.seek(0)
                file_bytes = self.image_file.read()
                result = storage.upload_file(key=key, data=file_bytes, content_type=content_type)

                self.image_url = result['url']

                if self.image_file.name:
                    try:
                        default_storage.delete(self.image_file.name)
                    except Exception:
                        pass

                self.image_file = None

            except Exception as e:
                logger.error(f"Storage 업로드 실패: {e}")
                if hasattr(self.image_file, 'url'):
                    self.image_url = self.image_file.url
                else:
                    self.image_url = 'https://via.placeholder.com/800x400/cccccc/666666?text=Upload+Failed'

        super().save(*args, **kwargs)
    
    def get_image_url(self):
        """이미지 URL 반환"""
        return self.image_url
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.title or self.alt}"
