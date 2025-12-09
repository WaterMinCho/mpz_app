import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')
django.setup()

from user.models import User
from notifications.models import PushToken

print("\n=== 등록된 사용자 목록 ===\n")
users = User.objects.all().order_by('id')
for user in users:
    token_count = PushToken.objects.filter(user=user, is_active=True).count()
    print(f"ID: {user.id:>4} | Username: {user.username:>20} | Email: {user.email or '(없음)':>30} | 토큰: {token_count}개")

print("\n=== 푸시 토큰이 있는 사용자만 ===\n")
users_with_tokens = User.objects.filter(pushtoken__is_active=True).distinct()
for user in users_with_tokens:
    tokens = PushToken.objects.filter(user=user, is_active=True)
    print(f"ID: {user.id:>4} | Username: {user.username:>20}")
    for token in tokens:
        print(f"  - 플랫폼: {token.platform or '(없음)':>8} | 토큰: {token.token[:40]}...")
