from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # 사용자별 실시간 알림
    re_path(
        # UUID 사용자 ID의 하이픈(-)까지 허용하도록 패턴 확장
        r"ws/notifications/(?P<user_id>[0-9a-fA-F-]+)/$",
        consumers.NotificationConsumer.as_asgi()
    ),
    
    # 관리자 브로드캐스트 알림
    re_path(
        r"ws/admin/notifications/$",
        consumers.BroadcastConsumer.as_asgi()
    ),
]
