from ninja import Schema, Field
from typing import List, Optional


class FavoriteToggleOut(Schema):
    """찜 토글 출력 스키마"""
    is_favorited: bool = Field(..., description="찜 상태")
    message: str = Field(..., description="결과 메시지")
    total_favorites: int = Field(..., description="총 찜 개수")


class FavoriteStatusOut(Schema):
    """찜 상태 확인 출력 스키마"""
    is_favorited: bool = Field(..., description="찜 상태")
    total_favorites: int = Field(..., description="총 찜 개수")


class CenterFavoriteOut(Schema):
    """찜한 센터 출력 스키마"""
    id: str = Field(..., description="센터 ID")
    name: str = Field(..., description="센터명")
    location: Optional[str] = Field(None, description="센터 위치 (공개 설정에 따라 조건부 노출)")
    region: Optional[str] = Field(None, description="센터 지역")
    phone_number: Optional[str] = Field(None, description="센터 전화번호")
    image_url: Optional[str] = Field(None, description="센터 이미지 URL")
    is_favorited: bool = Field(True, description="찜 상태 (항상 True)")
    favorited_at: str = Field(..., description="찜한 일시 (ISO 형식)")


class CenterFavoriteListOut(Schema):
    """찜한 센터 목록 출력 스키마"""
    centers: List[CenterFavoriteOut] = Field(..., description="찜한 센터 목록")
    total: int = Field(..., description="전체 찜한 센터 수")
    page: int = Field(..., description="현재 페이지 번호")
    limit: int = Field(..., description="페이지당 항목 수")
    total_pages: int = Field(..., description="전체 페이지 수")
    has_next: bool = Field(..., description="다음 페이지 존재 여부")
    has_prev: bool = Field(..., description="이전 페이지 존재 여부")


class AnimalFavoriteOut(Schema):
    """찜한 동물 출력 스키마"""
    id: str = Field(..., description="동물 ID")
    name: str = Field(..., description="동물 이름")
    breed: Optional[str] = Field(None, description="품종")
    age: Optional[int] = Field(None, description="나이 (개월)")
    is_female: bool = Field(..., description="암컷 여부")
    status: str = Field(..., description="동물 상태 (보호중, 입양대기, 입양완료)")
    personality: Optional[str] = Field(None, description="성격")
    center_id: str = Field(..., description="센터 ID")
    center_name: str = Field(..., description="센터명")
    is_favorited: bool = Field(True, description="찜 상태 (항상 True)")
    favorited_at: str = Field(..., description="찜한 일시 (ISO 형식)")


class AnimalFavoriteListOut(Schema):
    """찜한 동물 목록 출력 스키마"""
    animals: List[AnimalFavoriteOut] = Field(..., description="찜한 동물 목록")
    total: int = Field(..., description="전체 찜한 동물 수")
    page: int = Field(..., description="현재 페이지 번호")
    limit: int = Field(..., description="페이지당 항목 수")
    total_pages: int = Field(..., description="전체 페이지 수")
    has_next: bool = Field(..., description="다음 페이지 존재 여부")
    has_prev: bool = Field(..., description="이전 페이지 존재 여부")


class ErrorOut(Schema):
    """에러 응답 스키마"""
    error: str = Field(..., description="에러 메시지")
