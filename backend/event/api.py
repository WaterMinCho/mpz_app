from ninja import Router, Schema, Field
from django.http import HttpRequest
from django.core.mail import send_mail
from django.conf import settings

router = Router(tags=["Event"])


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
    response={200: dict, 400: dict, 500: dict},
)
async def event_apply(request: HttpRequest, data: EventApplyIn):
    full_address = data.address
    if data.address_detail:
        full_address += f" {data.address_detail}"

    subject = f"[MPZ 센터 신청] {data.center_name}"
    message = (
        f"센터명: {data.center_name}\n"
        f"운영자: {data.owner_name}\n"
        f"연락처: {data.phone}\n"
        f"주소: {full_address}\n"
        f"보호 동물 수: {data.animal_count}\n"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
    except Exception as e:
        return 500, {"success": False, "message": f"이메일 전송 실패: {str(e)}"}

    return 200, {"success": True, "message": "신청이 완료되었습니다."}
