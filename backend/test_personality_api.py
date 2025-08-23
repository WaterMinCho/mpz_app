"""성격 테스트 API 테스트 스크립트"""
import asyncio
import aiohttp
import json
import os
import django
from datetime import datetime, timedelta, timezone
import jwt

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

async def get_jwt_token():
    """테스트용 JWT 토큰 생성"""
    user = await User.objects.afirst()
    if not user:
        print("테스트용 사용자가 없습니다. 먼저 create_test_data 명령을 실행하세요.")
        return None
    
    # 간단한 JWT 토큰 생성
    payload = {
        'user_id': str(user.id),  # UUID를 문자열로 변환
        'username': user.username,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc)
    }
    
    # Django SECRET_KEY 사용
    secret_key = getattr(settings, 'SECRET_KEY', 'django-insecure-default-key')
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    return token

async def test_personality_test_api():
    """성격 테스트 API 테스트"""
    
    # JWT 토큰 가져오기
    token = await get_jwt_token()
    if not token:
        return
    
    print(f"테스트용 JWT 토큰: {token[:50]}...")
    
    # 테스트 데이터
    test_data = {
        "answers": {
            "당신의 생활 공간에 더 가까운 것은 어떤 편인가요?": "조용한 분위기를 좋아해요",
            "반려동물과 함께하는 시간을 어떻게 보내고 싶나요?": "산책이나 운동을 함께 하고 싶어요",
            "새로운 환경에 적응하는 편인가요?": "시간이 걸리지만 천천히 적응해요",
            "스트레스 받을 때 어떻게 해결하나요?": "혼자만의 시간을 갖고 싶어해요"
        }
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            # 성격 테스트 API 호출
            async with session.post(
                "http://localhost:8000/v1/favorites/personality-test",
                json=test_data,
                headers=headers
            ) as response:
                
                print(f"Response Status: {response.status}")
                print(f"Response Headers: {dict(response.headers)}")
                
                if response.status == 201:
                    result = await response.json()
                    print("✅ 성격 테스트 생성 성공!")
                    print(f"ID: {result['id']}")
                    print(f"완료 시간: {result['completed_at']}")
                    print(f"메시지: {result['message']}")
                    print(f"저장된 답변: {json.dumps(result['answers'], ensure_ascii=False, indent=2)}")
                else:
                    error_text = await response.text()
                    print(f"❌ API 호출 실패: {error_text}")
                    
        except Exception as e:
            print(f"❌ 테스트 중 오류 발생: {str(e)}")

async def main():
    """메인 테스트 실행"""
    print("🚀 성격 테스트 API 테스트 시작...")
    await test_personality_test_api()
    print("✅ 테스트 완료!")

if __name__ == "__main__":
    asyncio.run(main())
