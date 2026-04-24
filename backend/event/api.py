import re
import logging
from ninja import Router, Schema, Field
from django.http import HttpRequest
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)
router = Router(tags=["Event"])

# IP당 10분에 3회 제한
RATE_LIMIT_KEY_PREFIX = "event_apply_"
RATE_LIMIT_MAX = 3
RATE_LIMIT_WINDOW = 600  # 10분


def _sanitize(text: str) -> str:
    """이메일 헤더 인젝션 방지: 개행 문자 제거"""
    return re.sub(r"[\r\n]", " ", text).strip()


def _get_client_ip(request: HttpRequest) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


class EventApplyIn(Schema):
    center_name: str = Field(..., min_length=1, max_length=100)
    owner_name: str = Field(..., min_length=1, max_length=50)
    phone: str = Field(..., min_length=1, max_length=20)
    address: str = Field(..., min_length=1, max_length=300)
    address_detail: str = Field("", max_length=200)
    animal_count: str = Field(..., min_length=1, max_length=20)


@router.post(
    "/apply",
    summary="이벤트 센터 신청",
    description="민간보호센터 서비스 신청 폼을 이메일로 전송합니다.",
    response={200: dict, 400: dict, 429: dict, 500: dict},
)
async def event_apply(request: HttpRequest, data: EventApplyIn):
    # Rate limiting
    client_ip = _get_client_ip(request)
    cache_key = f"{RATE_LIMIT_KEY_PREFIX}{client_ip}"
    request_count = cache.get(cache_key, 0)

    if request_count >= RATE_LIMIT_MAX:
        return 429, {"success": False, "message": "잠시 후 다시 시도해주세요."}

    cache.set(cache_key, request_count + 1, RATE_LIMIT_WINDOW)

    full_address = _sanitize(data.address)
    if data.address_detail:
        full_address += f" {_sanitize(data.address_detail)}"

    subject = f"[MPZ 센터 신청] {_sanitize(data.center_name)}"
    message = (
        f"센터명: {_sanitize(data.center_name)}\n"
        f"운영자: {_sanitize(data.owner_name)}\n"
        f"연락처: {_sanitize(data.phone)}\n"
        f"주소: {full_address}\n"
        f"보호 동물 수: {_sanitize(data.animal_count)}\n"
    )

    try:
        await sync_to_async(send_mail)(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"이벤트 신청 이메일 전송 실패: {e}")
        return 500, {"success": False, "message": "이메일 전송에 실패했어요. 잠시 후 다시 시도해주세요."}

    return 200, {"success": True, "message": "신청이 완료됐어요."}
