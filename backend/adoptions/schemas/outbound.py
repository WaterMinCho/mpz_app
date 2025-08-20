from ninja import Schema
from typing import List, Optional


class PhoneVerificationOut(Schema):
    """전화번호 인증 응답 스키마"""
    success: bool = True                    # 성공 여부
    message: str = "인증이 완료되었습니다"     # 응답 메시지
    is_verified: Optional[bool] = True     # 인증 완료 여부 (선택적)


class UserSettingsOut(Schema):
    """사용자 설정 정보 응답 스키마"""
    phone: str = "010-1234-5678"           # 전화번호
    phone_verification: bool = True         # 전화번호 인증 완료 여부
    name: str = "홍길동"                    # 실명
    birth: str = "1990-01-01"              # 생년월일
    address: str = "서울시 강남구"           # 주소
    address_is_public: bool = False         # 주소 공개 여부


class AdoptionQuestionOut(Schema):
    """입양 질문 응답 스키마"""
    id: str = "uuid-string"                # 질문 ID
    content: str = "질문 내용"              # 질문 내용
    sequence: int = 1                      # 질문 순서


class AnimalInfoOut(Schema):
    """동물 정보 응답 스키마"""
    id: str = "uuid-string"                # 동물 ID
    name: str = "멍멍이"                    # 동물 이름
    status: str = "보호중"                  # 동물 상태 (보호중, 임시보호중, 입양완료 등)
    center_id: str = "uuid-string"         # 센터 ID
    center_name: str = "테스트 센터"         # 센터 이름


class CenterInfoOut(Schema):
    """센터 정보 응답 스키마"""
    has_monitoring: bool = True            # 모니터링 제공 여부
    monitoring_description: Optional[str] = "입양 후 모니터링을 제공합니다"  # 모니터링 설명
    adoption_guidelines: Optional[str] = "입양 유의사항입니다"              # 입양 가이드라인
    adoption_price: int = 0                # 입양 비용


class ContractTemplateOut(Schema):
    """계약서 템플릿 응답 스키마"""
    id: str = "uuid-string"                # 템플릿 ID
    title: str = "입양 계약서"              # 템플릿 제목
    content: str = "계약서 내용..."         # 템플릿 내용


class AdoptionPreCheckOut(Schema):
    """입양 신청 사전 확인 응답 스키마"""
    can_apply: bool = True                 # 입양 신청 가능 여부
    is_phone_verified: bool = True         # 전화번호 인증 상태
    needs_user_settings: bool = False      # 사용자 설정 입력 필요 여부
    animal: AnimalInfoOut                  # 동물 정보
    user_settings: Optional[UserSettingsOut] = None  # 사용자 설정 정보
    adoption_questions: List[AdoptionQuestionOut] = []  # 입양 질문 목록
    center_info: CenterInfoOut             # 센터 정보
    contract_template: Optional[ContractTemplateOut] = None  # 계약서 템플릿
    existing_application: bool = False     # 기존 신청 존재 여부


class AdoptionApplicationOut(Schema):
    """입양 신청 응답 스키마"""
    id: str = "uuid-string"                # 입양 신청 ID
    animal_id: str = "uuid-string"         # 동물 ID
    animal_name: str = "멍멍이"             # 동물 이름
    center_name: str = "테스트 센터"         # 센터 이름
    status: str = "신청"                   # 입양 상태 (신청, 미팅, 계약서작성, 입양완료, 모니터링, 취소)
    notes: Optional[str] = None            # 추가 메모
    created_at: str = "2024-01-01T00:00:00Z"  # 생성 시간 (ISO 8601)
    updated_at: str = "2024-01-01T00:00:00Z"  # 수정 시간 (ISO 8601)


class ContractSignOut(Schema):
    """계약서 서명 응답 스키마"""
    message: str = "계약서 서명이 완료되었습니다"  # 응답 메시지
    adoption_status: str = "입양완료"        # 입양 상태


class SuccessOut(Schema):
    """성공 응답 스키마"""
    success: bool = True                    # 성공 여부
    message: str = "처리가 완료되었습니다"     # 응답 메시지
