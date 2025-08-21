from ninja import Schema
from typing import Optional


class ContractTemplateCreateIn(Schema):
    """계약서 템플릿 생성 입력 스키마"""
    title: str
    description: Optional[str] = None
    content: str
    is_active: Optional[bool] = True


class ContractTemplateUpdateIn(Schema):
    """계약서 템플릿 수정 입력 스키마"""
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None
