from ninja import Schema
from typing import Optional


class ContractTemplateOut(Schema):
    """계약서 템플릿 출력 스키마"""
    id: str
    center_id: str
    title: str
    description: Optional[str] = None
    content: str
    is_active: bool
    created_at: str
    updated_at: str


class SuccessOut(Schema):
    """성공 응답 스키마"""
    message: str


class ErrorOut(Schema):
    """에러 응답 스키마"""
    error: str
