from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'AI 추천 테스트를 위한 샘플 데이터 생성'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=20,
            help='생성할 사용자 수 (기본값: 20)'
        )
        parser.add_argument(
            '--animals',
            type=int,
            default=20,
            help='생성할 동물 수 (기본값: 20)'
        )
    
    def handle(self, *args, **options):
        user_count = options['users']
        animal_count = options['animals']
        
        self.stdout.write(f'테스트 데이터 생성 시작 - 사용자: {user_count}명, 동물: {animal_count}마리')
        
        # 1. 보호소 데이터 생성
        centers = self.create_centers()
        self.stdout.write(f'보호소 {len(centers)}개 생성 완료')
        
        # 2. 사용자 데이터 생성
        users = self.create_users(user_count)
        self.stdout.write(f'사용자 {len(users)}명 생성 완료')
        
        # 3. 성격 테스트 데이터 생성
        personality_tests = self.create_personality_tests(users)
        self.stdout.write(f'성격 테스트 {len(personality_tests)}개 생성 완료')
        
        # 4. 동물 데이터 생성
        animals = self.create_animals(animal_count, centers)
        self.stdout.write(f'동물 {len(animals)}마리 생성 완료')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'테스트 데이터 생성 완료!\n'
                f'- 사용자: {len(users)}명\n'
                f'- 성격 테스트: {len(personality_tests)}개\n'  
                f'- 동물: {len(animals)}마리\n'
                f'- 보호소: {len(centers)}개'
            )
        )
    
    def create_centers(self):
        from centers.models import Center
        
        center_data = [
            {
                'name': '서울동물보호소',
                'location': '서울특별시 중랑구 용마산로 90-22',
                'phone_number': '02-2286-0777',
                'region': '서울',
                'description': '서울시 공식 동물보호소입니다.'
            },
            {
                'name': '부산유기동물보호소',
                'location': '부산광역시 강서구 대저2동',
                'phone_number': '051-970-2123',
                'region': '부산',
                'description': '부산시 유기동물 보호소입니다.'
            },
            {
                'name': '경기도동물보호센터',
                'location': '경기도 수원시 영통구 원천동',
                'phone_number': '031-8008-6264',
                'region': '경기',
                'description': '경기도 공식 동물보호센터입니다.'
            },
            {
                'name': '인천동물사랑센터',
                'location': '인천광역시 서구 원창동',
                'phone_number': '032-440-8321',
                'region': '인천',
                'description': '인천시 동물사랑센터입니다.'
            },
            {
                'name': '대전동물보호소',
                'location': '대전광역시 유성구 덕명동',
                'phone_number': '042-270-6400',
                'region': '대전',
                'description': '대전시 공식 동물보호소입니다.'
            }
        ]
        
        centers = []
        for data in center_data:
            center, created = Center.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            centers.append(center)
        
        return centers
    
    def create_users(self, count):
        first_names = [
            '지민', '서준', '민서', '하준', '도윤', '시우', '주원', '건우', '우진', '선우',
            '연우', '민준', '유준', '정우', '시윤', '준혁', '시후', '준서', '지후', '현우'
        ]
        
        last_names = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임']
        
        users = []
        for i in range(count):
            username = f'test_user_{i+1:02d}'
            email = f'{username}@test.com'
            
            # 중복 체크
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='testpass123',
                    nickname=f'{random.choice(last_names)}{random.choice(first_names)}',
                    phone_number=f'010-{random.randint(1000,9999)}-{random.randint(1000,9999)}',
                    user_type='일반사용자',
                    is_active=True,
                    terms_of_service=True,
                    privacy_policy_agreement=True,
                    terms_agreed_at=timezone.now()
                )
            users.append(user)
        
        return users
    
    def create_personality_tests(self, users):
        from favorites.models import PersonalityTest
        
        # 성격 유형별 답변 패턴
        personality_patterns = {
            '활발한_타입': {
                'energy_level': 5,
                'social_preference': 5,
                'activity_preference': 5,
                'training_patience': 4,
                'care_time': 4
            },
            '차분한_타입': {
                'energy_level': 2,
                'social_preference': 3,
                'activity_preference': 2,
                'training_patience': 5,
                'care_time': 5
            },
            '균형잡힌_타입': {
                'energy_level': 3,
                'social_preference': 4,
                'activity_preference': 3,
                'training_patience': 4,
                'care_time': 4
            },
            '사교적_타입': {
                'energy_level': 4,
                'social_preference': 5,
                'activity_preference': 4,
                'training_patience': 3,
                'care_time': 3
            },
            '독립적_타입': {
                'energy_level': 3,
                'social_preference': 2,
                'activity_preference': 3,
                'training_patience': 5,
                'care_time': 4
            }
        }
        
        personality_tests = []
        for user in users:
            # 기존 테스트가 있으면 스킵
            if PersonalityTest.objects.filter(user=user).exists():
                continue
                
            # 랜덤하게 성격 유형 선택
            personality_type = random.choice(list(personality_patterns.keys()))
            pattern = personality_patterns[personality_type]
            
            # 약간의 변동성 추가
            answers = {}
            for key, base_value in pattern.items():
                # ±1 범위의 변동성 (1-5 범위 유지)
                variation = random.randint(-1, 1)
                final_value = max(1, min(5, base_value + variation))
                answers[key] = final_value
            
            # 추가 질문들
            answers.update({
                'home_type': random.choice(['아파트', '단독주택', '원룸/오피스텔']),
                'family_size': random.randint(1, 4),
                'has_experience': random.choice([True, False]),
                'work_hours': random.randint(6, 10),
                'exercise_preference': random.choice(['실내', '실외', '둘다']),
                'noise_tolerance': random.randint(1, 5),
                'grooming_preference': random.randint(1, 5),
                'size_preference': random.choice(['소형', '중형', '대형', '상관없음']),
                'age_preference': random.choice(['새끼', '성년', '노년', '상관없음'])
            })
            
            test = PersonalityTest.objects.create(
                user=user,
                test_type='종합성격검사',
                answers=answers,
                result={
                    'personality_type': personality_type,
                    'compatibility_score': random.randint(75, 95),
                    'recommended_traits': self.get_recommended_traits(personality_type),
                    'care_level': self.get_care_level(pattern),
                    'activity_match': pattern['activity_preference']
                },
                completed_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            personality_tests.append(test)
        
        return personality_tests
    
    def get_recommended_traits(self, personality_type):
        trait_mapping = {
            '활발한_타입': ['활발함', '장난기많음', '운동량많음', '사교적'],
            '차분한_타입': ['온순함', '조용함', '차분함', '독립적'],
            '균형잡힌_타입': ['적응력좋음', '온순함', '영리함', '충성스러움'],
            '사교적_타입': ['사교적', '친화적', '활발함', '애교많음'],
            '독립적_타입': ['독립적', '차분함', '영리함', '경계심있음']
        }
        return trait_mapping.get(personality_type, ['온순함', '충성스러움'])
    
    def get_care_level(self, pattern):
        avg_care = (pattern['training_patience'] + pattern['care_time']) / 2
        if avg_care >= 4.5:
            return '높음'
        elif avg_care >= 3.5:
            return '중간'
        else:
            return '낮음'
    
    def create_animals(self, count, centers):
        from animals.models import Animal
        
        # 강아지 품종과 특성 데이터
        dog_breeds = [
            {
                'breed': '골든 리트리버',
                'size': '대형',
                'personality_base': ['온순함', '친화적', '활발함', '영리함'],
                'activity_level': (4, 5),
                'sociability': (4, 5),
                'separation_anxiety': (2, 4),
                'basic_training': (4, 5)
            },
            {
                'breed': '말티즈',
                'size': '소형',
                'personality_base': ['애교많음', '활발함', '경계심있음'],
                'activity_level': (3, 4),
                'sociability': (3, 4),
                'separation_anxiety': (3, 5),
                'basic_training': (2, 4)
            },
            {
                'breed': '시바견',
                'size': '중형',
                'personality_base': ['독립적', '영리함', '충성스러움', '경계심있음'],
                'activity_level': (3, 4),
                'sociability': (2, 3),
                'separation_anxiety': (1, 2),
                'basic_training': (3, 4)
            },
            {
                'breed': '포메라니안',
                'size': '소형',
                'personality_base': ['활발함', '애교많음', '장난기많음'],
                'activity_level': (4, 5),
                'sociability': (4, 5),
                'separation_anxiety': (3, 4),
                'basic_training': (2, 3)
            },
            {
                'breed': '비글',
                'size': '중형',
                'personality_base': ['활발함', '친화적', '호기심많음', '운동량많음'],
                'activity_level': (4, 5),
                'sociability': (4, 5),
                'separation_anxiety': (2, 3),
                'basic_training': (3, 4)
            },
            {
                'breed': '푸들',
                'size': '중형',
                'personality_base': ['영리함', '활발함', '사교적', '학습능력좋음'],
                'activity_level': (3, 4),
                'sociability': (4, 5),
                'separation_anxiety': (2, 3),
                'basic_training': (4, 5)
            },
            {
                'breed': '진돗개',
                'size': '중형',
                'personality_base': ['충성스러움', '독립적', '경계심있음', '영리함'],
                'activity_level': (3, 4),
                'sociability': (2, 3),
                'separation_anxiety': (1, 2),
                'basic_training': (3, 5)
            },
            {
                'breed': '치와와',
                'size': '소형',
                'personality_base': ['경계심있음', '애교많음', '보호본능있음'],
                'activity_level': (2, 3),
                'sociability': (2, 4),
                'separation_anxiety': (3, 5),
                'basic_training': (2, 3)
            }
        ]
        
        # 이름 후보
        dog_names = [
            '몽이', '보리', '코코', '루루', '마루', '초코', '쿠키', '마음이', '별이', '구름이',
            '하늘이', '바다', '모카', '라떼', '두부', '콩이', '밤이', '눈이', '달이', '해피'
        ]
        
        animals = []
        for i in range(count):
            breed_info = random.choice(dog_breeds)
            name = f"{random.choice(dog_names)}{i+1:02d}" if i > len(dog_names) else random.choice(dog_names)
            
            # 나이와 체중 설정
            age_months = random.randint(6, 120)  # 6개월 ~ 10년
            if breed_info['size'] == '소형':
                weight = round(random.uniform(2.0, 8.0), 1)
            elif breed_info['size'] == '중형':
                weight = round(random.uniform(8.0, 25.0), 1)
            else:  # 대형
                weight = round(random.uniform(25.0, 45.0), 1)
            
            # 성격 특성 생성
            personality_traits = random.sample(breed_info['personality_base'], 
                                             random.randint(2, len(breed_info['personality_base'])))
            
            # 중복 체크
            if Animal.objects.filter(name=name, breed=breed_info['breed']).exists():
                continue
                
            animal = Animal.objects.create(
                name=name,
                breed=breed_info['breed'],
                age=age_months,
                weight=weight,
                is_female=not random.choice([True, False]),  # is_male -> is_female로 변경하고 반대로
                neutering=random.choice([True, False]),  # is_neutered -> neutering
                vaccination=random.choice([True, False]),
                heartworm=random.choice([True, False]),
                
                # 성격 및 특성
                personality=', '.join(personality_traits),
                description=self.generate_description(name, breed_info['breed'], personality_traits),
                special_needs=self.generate_special_needs(),
                health_notes=self.generate_health_notes(),
                
                # 수치형 특성
                activity_level=random.randint(*breed_info['activity_level']),
                sensitivity=random.randint(1, 5),
                sociability=random.randint(*breed_info['sociability']),
                separation_anxiety=random.randint(*breed_info['separation_anxiety']),
                basic_training=random.randint(*breed_info['basic_training']),
                
                # 기타 정보
                trainer_comment=self.generate_trainer_comment(personality_traits),
                center=random.choice(centers),
                adoption_fee=random.randint(100000, 500000),
                found_location=self.generate_location(),
                admission_date=timezone.now() - timedelta(days=random.randint(10, 365)),
                
                # 상태
                status='보호중',
                is_public=True
            )
            animals.append(animal)
        
        return animals
    
    def generate_description(self, name, breed, traits):
        descriptions = [
            f"{name}는 {breed} 품종으로 {', '.join(traits[:2])}한 성격을 가지고 있어요.",
            f"사랑스러운 {name}이가 새 가족을 기다리고 있습니다.",
            f"{name}는 건강하고 활발한 아이로, 좋은 가정에서 사랑받고 싶어해요.",
            f"매력적인 {name}는 사람을 좋아하고 잘 따라요."
        ]
        return random.choice(descriptions)
    
    def generate_special_needs(self):
        needs = [
            None,
            "정기적인 운동이 필요합니다",
            "털 관리가 필요합니다",
            "소음에 민감하니 조용한 환경이 좋습니다",
            "다른 동물과의 사회화가 필요합니다",
            "기본 훈련이 더 필요합니다"
        ]
        return random.choice(needs)
    
    def generate_health_notes(self):
        notes = [
            None,
            "건강한 상태입니다",
            "정기 검진 필요",
            "피부 관리 주의",
            "무릎 관절 주의 필요",
            "심장 건강 체크 필요"
        ]
        return random.choice(notes)
    
    def generate_trainer_comment(self, traits):
        if '활발함' in traits:
            return "에너지가 넘치는 아이로 충분한 운동과 놀이가 필요해요."
        elif '온순함' in traits:
            return "매우 순하고 사람을 잘 따르는 아이입니다."
        elif '독립적' in traits:
            return "독립적인 성향이지만 주인에게는 충성스러워요."
        else:
            return "사랑스럽고 건강한 아이입니다."
    
    def generate_location(self):
        locations = [
            "서울시 강남구 일대",
            "서울시 마포구 공원 근처",
            "경기도 수원시 주택가",
            "부산시 해운대구 해변가",
            "인천시 부평구 상가 앞",
            "대전시 유성구 대학가"
        ]
        return random.choice(locations)
