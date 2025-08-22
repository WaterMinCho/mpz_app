from ninja import Schema
from typing import Optional, List

from .inbound import ContractTemplateCreateIn


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


class ProcedureSettingsOut(Schema):
    """프로시저 설정 출력 스키마"""
    has_monitoring: Optional[bool] = None
    monitoring_period_months: Optional[int] = None
    monitoring_interval_days: Optional[int] = None
    monitoring_description: Optional[str] = None
    adoption_guidelines: Optional[str] = None
    adoption_procedure: Optional[str] = None
    contract_templates: List[ContractTemplateOut] = []
