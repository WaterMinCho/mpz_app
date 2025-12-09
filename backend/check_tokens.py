import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')
django.setup()

from user.models import User
from notifications.models import PushToken

print("\n=== 푸시 토큰이 등록된 사용자 ===\n")
tokens = PushToken.objects.filter(is_active=True).select_related('user')
if not tokens.exists():
    print("등록된 푸시 토큰이 없습니다.")
else:
    for token in tokens:
        print(f"사용자 ID: {str(token.user.id):>36} | Username: {token.user.username:>20}")
        print(f"  플랫폼: {token.platform or '(없음)':>8} | 토큰: {token.token[:50]}...")
        print(f"  등록일: {token.last_used or token.created_at}")
        print()

