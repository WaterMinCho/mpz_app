from ninja import Schema
from typing import Optional
from datetime import date
from pydantic import Field
from decimal import Decimal


class AnimalCreateIn(Schema):
    """동물 등록 입력 스키마"""
    name: str
    is_female: bool
    age: Optional[int] = Field(None, ge=0, le=300, description="나이 (개월 단위, 0-300개월)")
    weight: Optional[Decimal] = Field(None, ge=Decimal('0.01'), le=Decimal('999.99'), description="체중 (kg, 0.01-999.99kg)")
    color: Optional[str] = None
    breed: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "보호중"
    activity_level: Optional[str] = None
    sensitivity: Optional[str] = None
    sociability: Optional[str] = None
    separation_anxiety: Optional[str] = None
    special_notes: Optional[str] = None
    health_notes: Optional[str] = None
    basic_training: Optional[str] = None
    trainer_comment: Optional[str] = None
    announce_number: Optional[str] = None
    announcement_date: Optional[date] = None
    found_location: Optional[str] = None
    personality: Optional[str] = None


class AnimalUpdateIn(Schema):
    """동물 정보 수정 입력 스키마"""
    name: Optional[str] = None
    is_female: Optional[bool] = None
    age: Optional[int] = Field(None, ge=0, le=300, description="나이 (개월 단위, 0-300개월)")
    weight: Optional[Decimal] = Field(None, ge=Decimal('0.01'), le=Decimal('999.99'), description="체중 (kg, 0.01-999.99kg)")
    color: Optional[str] = None
    breed: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    activity_level: Optional[str] = None
    sensitivity: Optional[str] = None
    sociability: Optional[str] = None
    separation_anxiety: Optional[str] = None
    special_notes: Optional[str] = None
    health_notes: Optional[str] = None
    basic_training: Optional[str] = None
    trainer_comment: Optional[str] = None
    announce_number: Optional[str] = None
    announcement_date: Optional[date] = None
    found_location: Optional[str] = None
    personality: Optional[str] = None


class AnimalStatusUpdateIn(Schema):
    """동물 상태 변경 입력 스키마"""
    status: str
    reason: Optional[str] = None


class AnimalListQueryIn(Schema):
    """동물 목록 조회 쿼리 스키마"""
    status: Optional[str] = None
    center_id: Optional[str] = None
    gender: Optional[str] = None  # "female" or "male"
    weight_min: Optional[Decimal] = Field(None, ge=Decimal('0.01'), le=Decimal('999.99'), description="최소 체중 (kg)")
    weight_max: Optional[Decimal] = Field(None, ge=Decimal('0.01'), le=Decimal('999.99'), description="최대 체중 (kg)")
    age_min: Optional[int] = Field(None, ge=0, le=300, description="최소 나이 (개월)")
    age_max: Optional[int] = Field(None, ge=0, le=300, description="최대 나이 (개월)")
    has_trainer_comment: Optional[str] = None  # "true" or "false"
    breed: Optional[str] = None
    region: Optional[str] = None


class RelatedAnimalsQueryIn(Schema):
    """관련 동물 조회 쿼리 스키마"""
    limit: Optional[int] = 6