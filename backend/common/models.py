import uuid
from django.db import models


class BaseModel(models.Model):
    """Common Model Definition"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="고유 식별자")
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성일")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정일")

    class Meta:
        abstract = True
