#!/usr/bin/env python
"""
사용자 ID 조회 스크립트
사용법: python manage.py shell < get_user_id.py
또는: python get_user_id.py (Django 설정이 올바르게 되어 있을 때)
"""
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')
django.setup()

from user.models import User

print("\n=== 등록된 사용자 목록 ===\n")
users = User.objects.all().order_by('id')

if not users.exists():
    print("등록된 사용자가 없습니다.")
else:
    for user in users:
        print(f"ID: {user.id:>4} | Username: {user.username:>20} | Email: {user.email or '(없음)':>30} | 타입: {user.user_type or '(없음)'}")

print("\n=== 푸시 토큰이 등록된 사용자 ===\n")
from notifications.models import PushToken

users_with_tokens = User.objects.filter(pushtoken__is_active=True).distinct()
if not users_with_tokens.exists():
    print("푸시 토큰이 등록된 사용자가 없습니다.")
else:
    for user in users_with_tokens:
        tokens = PushToken.objects.filter(user=user, is_active=True)
        print(f"ID: {user.id:>4} | Username: {user.username:>20} | 토큰 수: {tokens.count()}개")
        for token in tokens:
            print(f"  - 플랫폼: {token.platform or '(없음)':>8} | 토큰: {token.token[:30]}...")

print("\n")
