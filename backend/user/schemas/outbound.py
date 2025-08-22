from ninja import Schema, ModelSchema, Field
from user.models import User


class UserMeOut(Schema):
    username: str = Field(..., description="사용자 아이디")
    status: str = Field(..., description="사용자 상태")

class UserLoginOut(Schema):
    access_token: str = Field(..., description="액세스 토큰")
    refresh_token: str = Field(..., description="리프레시 토큰")
    status: str = Field(..., description="로그인 상태")


class UserRefreshTokenOut(Schema):
    access_token: str = Field(..., description="새로운 액세스 토큰")
    refresh_token: str = Field(..., description="새로운 리프레시 토큰")


class UserListOut(Schema):
    """사용자 목록 응답 스키마"""
    id: str = Field(..., description="사용자 ID")
    username: str = Field(..., description="사용자 아이디")
    email: str = Field(..., description="이메일 주소")
    nickname: str = Field(..., description="닉네임")
    user_type: str = Field(..., description="사용자 유형")
    status: str = Field(..., description="사용자 상태")
    created_at: str = Field(..., description="생성일시 (ISO 형식)")
    updated_at: str = Field(..., description="수정일시 (ISO 형식)")


class SuccessOut(Schema):
    detail: str = Field(..., description="성공 메시지")