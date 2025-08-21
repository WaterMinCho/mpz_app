from ninja import Schema
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class AnimalImageOut(Schema):
    """동물 이미지 출력 스키마"""
    id: str
    image_url: str
    is_primary: bool
    sequence: int


class AnimalOut(Schema):
    """동물 출력 스키마"""
    id: str
    name: str
    is_female: bool
    age: Optional[int] = None
    weight: Optional[Decimal] = None
    color: Optional[str] = None
    breed: Optional[str] = None
    description: Optional[str] = None
    status: str
    waiting_days: int = 0
    activity_level: Optional[str] = None
    sensitivity: Optional[str] = None
    sociability: Optional[str] = None
    separation_anxiety: Optional[str] = None
    special_notes: Optional[str] = None
    health_notes: Optional[str] = None
    basic_training: Optional[str] = None
    trainer_comment: Optional[str] = None
    announce_number: Optional[str] = None
    announcement_date: Optional[str] = None
    found_location: Optional[str] = None
    personality: Optional[str] = None
    center_id: str
    animal_images: List[AnimalImageOut] = []
    created_at: str
    updated_at: str


class AnimalListOut(Schema):
    """동물 목록 출력 스키마"""
    animals: List[AnimalOut]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_prev: bool


class AnimalStatusUpdateOut(Schema):
    """동물 상태 변경 출력 스키마"""
    id: str
    name: str
    previous_status: str
    new_status: str
    updated_at: str
    message: str


class BreedsOut(Schema):
    """품종 목록 출력 스키마"""
    breeds: List[str]
    total: int


class RelatedAnimalsOut(Schema):
    """관련 동물 목록 출력 스키마"""
    animals: List[AnimalOut]
    total: int


class SuccessOut(Schema):
    """성공 응답 스키마"""
    message: str


class ErrorOut(Schema):
    """에러 응답 스키마"""
    error: str