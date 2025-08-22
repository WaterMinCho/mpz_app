from ninja import Schema, Field
from typing import Optional
from datetime import date
from decimal import Decimal


class AnimalCreateIn(Schema):
    """동물 등록 입력 스키마"""
    name: str = Field(..., min_length=1, max_length=50, description="동물 이름")
    is_female: bool = Field(..., description="암컷 여부")
    age: Optional[int] = Field(None, ge=0, le=300, description="나이 (개월 단위, 0-300개월)")
    weight: Optional[Decimal] = Field(None, ge=Decimal('0.01'), le=Decimal('999.99'), description="체중 (kg, 0.01-999.99kg)")
    color: Optional[str] = Field(None, max_length=50, description="색상")
    breed: Optional[str] = Field(None, max_length=50, description="품종")
    description: Optional[str] = Field(None, max_length=1000, description="동물 설명")
    status: Optional[str] = Field("보호중", description="동물 상태 (보호중, 입양대기, 입양완료)")
    activity_level: Optional[str] = Field(None, max_length=50, description="활동량 수준")
    sensitivity: Optional[str] = Field(None, max_length=50, description="예민함 정도")
    sociability: Optional[str] = Field(None, max_length=50, description="사회성")
    separation_anxiety: Optional[str] = Field(None, max_length=50, description="분리불안 정도")
    special_notes: Optional[str] = Field(None, max_length=1000, description="특이사항")
    health_notes: Optional[str] = Field(None, max_length=1000, description="건강 정보")
    basic_training: Optional[str] = Field(None, max_length=500, description="기본 훈련 상태")
    trainer_comment: Optional[str] = Field(None, max_length=1000, description="훈련사 코멘트")
    announce_number: Optional[str] = Field(None, max_length=50, description="공고번호")
    announcement_date: Optional[date] = Field(None, description="공고일")
    found_location: Optional[str] = Field(None, max_length=200, description="발견 장소")
    personality: Optional[str] = Field(None, max_length=500, description="성격")


class AnimalUpdateIn(Schema):
    """동물 정보 수정 입력 스키마"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="동물 이름")
    is_female: Optional[bool] = Field(None, description="암컷 여부")
    age: Optional[int] = Field(None, ge=0, le=300, description="나이 (개월 단위, 0-300개월)")
    weight: Optional[Decimal] = Field(None, ge=Decimal('0.01'), le=Decimal('999.99'), description="체중 (kg, 0.01-999.99kg)")
    color: Optional[str] = Field(None, max_length=50, description="색상")
    breed: Optional[str] = Field(None, max_length=50, description="품종")
    description: Optional[str] = Field(None, max_length=1000, description="동물 설명")
    status: Optional[str] = Field(None, description="동물 상태 (보호중, 입양대기, 입양완료)")
    activity_level: Optional[str] = Field(None, max_length=50, description="활동량 수준")
    sensitivity: Optional[str] = Field(None, max_length=50, description="예민함 정도")
    sociability: Optional[str] = Field(None, max_length=50, description="사회성")
    separation_anxiety: Optional[str] = Field(None, max_length=50, description="분리불안 정도")
    special_notes: Optional[str] = Field(None, max_length=1000, description="특이사항")
    health_notes: Optional[str] = Field(None, max_length=1000, description="건강 정보")
    basic_training: Optional[str] = Field(None, max_length=500, description="기본 훈련 상태")
    trainer_comment: Optional[str] = Field(None, max_length=1000, description="훈련사 코멘트")
    announce_number: Optional[str] = Field(None, max_length=50, description="공고번호")
    announcement_date: Optional[date] = Field(None, description="공고일")
    found_location: Optional[str] = Field(None, max_length=200, description="발견 장소")
    personality: Optional[str] = Field(None, max_length=500, description="성격")


class AnimalStatusUpdateIn(Schema):
    """동물 상태 변경 입력 스키마"""
    status: str = Field(..., description="변경할 동물 상태 (보호중, 입양대기, 입양완료)")
    reason: Optional[str] = Field(None, max_length=500, description="상태 변경 사유")


class AnimalListQueryIn(Schema):
    """동물 목록 조회 쿼리 스키마"""
    status: Optional[str] = Field(None, description="동물 상태 필터링 (보호중, 입양대기, 입양완료)")
    center_id: Optional[str] = Field(None, description="센터 ID 필터링")
    gender: Optional[str] = Field(None, pattern="^(female|male)$", description="성별 필터링 (female or male)")
    weight_min: Optional[Decimal] = Field(None, ge=Decimal('0.01'), le=Decimal('999.99'), description="최소 체중 (kg)")
    weight_max: Optional[Decimal] = Field(None, ge=Decimal('0.01'), le=Decimal('999.99'), description="최대 체중 (kg)")
    age_min: Optional[int] = Field(None, ge=0, le=300, description="최소 나이 (개월)")
    age_max: Optional[int] = Field(None, ge=0, le=300, description="최대 나이 (개월)")
    has_trainer_comment: Optional[str] = Field(None, pattern="^(true|false)$", description="훈련사 코멘트 존재 여부 (true or false)")
    breed: Optional[str] = Field(None, max_length=50, description="품종 필터링")
    region: Optional[str] = Field(None, max_length=50, description="지역 필터링")


class RelatedAnimalsQueryIn(Schema):
    """관련 동물 조회 쿼리 스키마"""
    limit: Optional[int] = Field(6, ge=1, le=20, description="조회할 관련 동물 수 (최대 20)")