#!/usr/bin/env python
"""
AI 동물 추천 통합 테스트 스크립트 - 전체 플로우 테스트
"""
import requests
import json
import sys
import os
from datetime import datetime
import uuid

# Django 프로젝트 설정
import django
sys.path.append('/Users/eomseongmin/mpz_fullstack/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')
django.setup()

from user.models import User
from user.utils import get_access_token
from animals.models import Animal
from centers.models import Center
from favorites.models import PersonalityTest

class AIRecommendationIntegratedTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.test_user = None
        self.test_center = None
        self.test_animals = []
        
    def step1_create_user(self):
        """1단계: 테스트 사용자 생성"""
        print("🔧 1단계: 테스트 사용자 생성 중...")
        
        # 고유한 사용자 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        username = f"ai_test_user_{timestamp}"
        
        try:
            # 기존 사용자가 있으면 삭제
            existing_user = User.objects.filter(username=username).first()
            if existing_user:
                existing_user.delete()
                
            # 새 사용자 생성
            self.test_user = User.objects.create_user(
                username=username,
                email=f"{username}@test.com",
                nickname=f"AI테스트_{timestamp}",
                password="testpass123",
                user_type="일반사용자",
                phone_number=f"010-{timestamp[-4:]}-{timestamp[-4:]}"
            )
            
            # JWT 토큰 생성
            payload = {
                "user_id": str(self.test_user.id),
                "username": self.test_user.username,
                "user_type": self.test_user.user_type
            }
            access_token, _ = get_access_token(payload)
            self.token = access_token
            
            print(f"✅ 사용자 생성 완료: {self.test_user.nickname} (ID: {self.test_user.id})")
            return True
            
        except Exception as e:
            print(f"❌ 사용자 생성 실패: {str(e)}")
            return False
    
    def step2_create_shelter_and_animals(self):
        """2단계: 보호소 및 반려견 데이터 생성"""
        print("🏠 2단계: 보호소 및 반려견 데이터 생성 중...")
        
        try:
            # 테스트용 보호소 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.test_center = Center.objects.create(
                name=f"AI테스트보호소_{timestamp}",
                region="서울특별시",
                location="서울시 강남구 테스트동 123",
                phone_number=f"02-{timestamp[-4:]}-{timestamp[-4:]}",
                is_public=True
            )
            
            # 다양한 성격의 반려견 데이터 생성
            animals_data = [
                {
                    "name": "활발이",
                    "breed": "골든 리트리버",
                    "personality": ["활발함", "사교적", "친근함"],
                    "age": 2,
                    "is_female": False
                },
                {
                    "name": "조용이",
                    "breed": "푸들",
                    "personality": ["온순함", "차분함", "독립적"],
                    "age": 4,
                    "is_female": True
                },
                {
                    "name": "장난이",
                    "breed": "비글",
                    "personality": ["장난기많음", "활발함", "호기심많음"],
                    "age": 1,
                    "is_female": False
                },
                {
                    "name": "순둥이",
                    "breed": "말티즈",
                    "personality": ["온순함", "애교많음", "차분함"],
                    "age": 3,
                    "is_female": True
                },
                {
                    "name": "용감이",
                    "breed": "진돗개",
                    "personality": ["용감함", "충성스러움", "독립적"],
                    "age": 5,
                    "is_female": False
                }
            ]
            
            for animal_data in animals_data:
                animal = Animal.objects.create(
                    center=self.test_center,
                    name=animal_data["name"],
                    breed=animal_data["breed"],
                    personality=animal_data["personality"],
                    age=animal_data["age"],
                    is_female=animal_data["is_female"],
                    status="보호중",
                    found_location=f"서울시 {animal_data['name']} 발견지역",
                    admission_date=datetime.now().date()
                )
                self.test_animals.append(animal)
            
            print(f"✅ 보호소 생성 완료: {self.test_center.name}")
            print(f"✅ 반려견 {len(self.test_animals)}마리 생성 완료")
            for animal in self.test_animals:
                print(f"   - {animal.name} ({animal.breed}): {', '.join(animal.personality)}")
            
            return True
            
        except Exception as e:
            print(f"❌ 보호소/동물 생성 실패: {str(e)}")
            return False
    
    def step3_create_personality_test(self):
        """3단계: 사용자 성격 테스트 데이터 생성"""
        print("🧠 3단계: 사용자 성격 테스트 데이터 생성 중...")
        
        if not self.test_user:
            print("❌ 테스트 사용자가 없습니다.")
            return False
            
        url = f"{self.base_url}/v1/favorites/personality-test"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        # 성격 테스트 답변 데이터
        test_data = {
            "answers": {
                "당신의 생활 공간에 더 가까운 것은 어떤 편인가요?": "활발하고 넓은 공간을 좋아해요",
                "반려동물과 함께하는 시간을 어떻게 보내고 싶나요?": "산책이나 운동을 함께 하고 싶어요",
                "새로운 환경에 적응하는 편인가요?": "빠르게 적응하는 편이에요",
                "스트레스 받을 때 어떻게 해결하나요?": "활동적인 것을 하며 해결해요",
                "평소 성격은 어떤 편인가요?": "외향적이고 사교적인 편이에요",
                "반려동물에게 원하는 성격은?": "활발하고 친근한 성격이 좋아요"
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=test_data)
            
            if response.status_code == 201:
                result = response.json()
                print("✅ 성격 테스트 생성 성공!")
                print(f"   테스트 ID: {result['id']}")
                print(f"   완료 시간: {result['completed_at']}")
                return True
            else:
                print(f"❌ 성격 테스트 생성 실패: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 성격 테스트 생성 중 오류: {str(e)}")
            return False
    
    def step4_run_ai_recommendation(self):
        """4단계: AI 추천 실행"""
        print("🤖 4단계: AI 동물 추천 실행 중...")
        
        if not self.token:
            print("❌ 토큰이 없습니다.")
            return False
            
        url = f"{self.base_url}/v1/ai/recommend"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        # 추천 요청 데이터
        data = {
            'limit': 3,
            'preferences': {
                "활동_수준": "높음",
                "크기_선호": "중형",
                "성격_선호": ["활발함", "사교적"]
            }
        }
        
        print(f"요청 데이터: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        try:
            response = requests.post(url, headers=headers, json=data)
            print(f"응답 코드: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ AI 추천 성공!")
                print("📊 추천 결과:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                
                # 저장 상태 확인
                if result.get('save_status', {}).get('saved'):
                    print("✅ 추천 결과가 성격 테스트에 저장되었습니다!")
                else:
                    print("⚠️ 추천 결과 저장 실패:", result.get('save_status', {}))
                
                return True
            else:
                print(f"❌ AI 추천 실패: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ 서버에 연결할 수 없습니다. Django 서버가 실행 중인지 확인하세요.")
            return False
        except Exception as e:
            print(f"❌ AI 추천 중 오류: {str(e)}")
            return False
    
    def cleanup(self):
        """테스트 데이터 정리"""
        print("🧹 테스트 데이터 정리 중...")
        
        try:
            if self.test_animals:
                for animal in self.test_animals:
                    animal.delete()
                print(f"✅ 테스트 동물 {len(self.test_animals)}마리 삭제 완료")
            
            if self.test_center:
                self.test_center.delete()
                print("✅ 테스트 보호소 삭제 완료")
            
            if self.test_user:
                # 관련된 PersonalityTest도 함께 삭제됨 (CASCADE)
                self.test_user.delete()
                print("✅ 테스트 사용자 삭제 완료")
                
        except Exception as e:
            print(f"⚠️ 데이터 정리 중 오류: {str(e)}")
    
    def run_full_integrated_test(self, cleanup_after=True):
        """전체 통합 테스트 실행"""
        print("🚀 AI 동물 추천 통합 테스트 시작")
        print("=" * 60)
        
        success_steps = 0
        total_steps = 4
        
        try:
            # 1단계: 사용자 생성
            if self.step1_create_user():
                success_steps += 1
            else:
                return False
            
            # 2단계: 보호소 및 동물 생성
            if self.step2_create_shelter_and_animals():
                success_steps += 1
            else:
                return False
            
            # 3단계: 성격 테스트 생성
            if self.step3_create_personality_test():
                success_steps += 1
            else:
                return False
            
            # 4단계: AI 추천 실행
            if self.step4_run_ai_recommendation():
                success_steps += 1
            
            print("=" * 60)
            print(f"🏁 테스트 완료! ({success_steps}/{total_steps} 단계 성공)")
            
            if success_steps == total_steps:
                print("🎉 모든 단계가 성공적으로 완료되었습니다!")
            else:
                print("⚠️ 일부 단계에서 오류가 발생했습니다.")
            
        finally:
            if cleanup_after:
                print("\n" + "=" * 60)
                self.cleanup()
        
        return success_steps == total_steps

def main():
    tester = AIRecommendationIntegratedTester()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "no-cleanup":
            # 테스트 데이터를 삭제하지 않고 테스트 실행
            tester.run_full_integrated_test(cleanup_after=False)
        elif sys.argv[1] == "cleanup-only":
            # 기존 테스트 데이터만 정리
            tester.cleanup()
        else:
            print("사용법:")
            print("  python test_ai_api.py           # 전체 통합 테스트 (테스트 후 데이터 정리)")
            print("  python test_ai_api.py no-cleanup # 전체 통합 테스트 (데이터 보존)")
            print("  python test_ai_api.py cleanup-only # 기존 테스트 데이터만 정리")
    else:
        # 기본: 전체 통합 테스트 실행 (테스트 후 정리)
        tester.run_full_integrated_test()

if __name__ == "__main__":
    main()
