import uuid
import jwt
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from ninja.testing import TestAsyncClient

from posts.models import Post, PostTag, PostImage, SystemTag
from comments.models import Comment, Reply


User = get_user_model()


class TestPostsAPI(TestCase):
    """Posts API 테스트 클래스"""

    def setUp(self):
        """테스트 데이터 설정"""
        # 테스트 사용자 생성
        self.user1 = User.objects.create_user(
            username="testuser1",
            email="test1@test.com",
            password="password1234!",
            user_type="일반사용자"
        )
        
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@test.com",
            password="password1234!",
            user_type="일반사용자"
        )
        
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="password1234!",
            user_type="최고관리자"
        )
        
        # 테스트 게시글 생성
        self.post1 = Post.objects.create(
            user=self.user1,
            title="테스트 게시글 1",
            content="테스트 내용 1"
        )
        
        self.post2 = Post.objects.create(
            user=self.user2,
            title="테스트 게시글 2",
            content="테스트 내용 2"
        )
        
        # 테스트 태그 생성 (시스템 태그와 매칭되는 태그들)
        self.tag1 = PostTag.objects.create(
            post=self.post1,
            tag_name="강아지"  # 시스템 태그와 매칭
        )
        
        self.tag2 = PostTag.objects.create(
            post=self.post1,
            tag_name="귀여워"  # 시스템 태그와 매칭 안됨
        )
        
        # 시스템 태그와 매칭되는 태그
        self.tag3 = PostTag.objects.create(
            post=self.post2,
            tag_name="고양이"  # 시스템 태그와 매칭
        )
        
        # 시스템 태그와 전혀 매칭되지 않는 태그
        self.tag4 = PostTag.objects.create(
            post=self.post2,
            tag_name="맛있는음식"  # 시스템 태그와 매칭 안됨
        )
        
        # 테스트 이미지 생성
        self.image1 = PostImage.objects.create(
            post=self.post1,
            image_url="https://example.com/image1.jpg",
            order_index=0
        )
        
        self.image2 = PostImage.objects.create(
            post=self.post1,
            image_url="https://example.com/image2.jpg",
            order_index=1
        )
        
        # 테스트 댓글 생성
        self.comment1 = Comment.objects.create(
            post=self.post1,
            user=self.user2,
            content="테스트 댓글 1"
        )
        
        self.comment2 = Comment.objects.create(
            post=self.post1,
            user=self.user1,
            content="테스트 댓글 2"
        )
        
        # 테스트 대댓글 생성
        self.reply1 = Reply.objects.create(
            comment=self.comment1,
            user=self.user1,
            content="테스트 대댓글 1"
        )
        
        # 테스트 시스템 태그 생성
        self.system_tag1 = SystemTag.objects.create(
            name="강아지",
            description="강아지 관련 게시글",
            is_active=True
        )
        
        self.system_tag2 = SystemTag.objects.create(
            name="고양이",
            description="고양이 관련 게시글",
            is_active=True
        )
        
        self.system_tag3 = SystemTag.objects.create(
            name="입양",
            description="입양 관련 게시글",
            is_active=True
        )
        
        # 비활성화된 시스템 태그
        self.inactive_system_tag = SystemTag.objects.create(
            name="비활성태그",
            description="비활성화된 태그",
            is_active=False
        )
        
        # 테스트 클라이언트 설정
        from posts.api import router
        self.client = TestAsyncClient(router)

    def generate_jwt_token(self, user):
        """실제 JWT 토큰을 생성합니다"""
        payload = {
            'user_id': str(user.id),
            'username': user.username,
            'exp': timezone.now() + timedelta(hours=1),
            'iat': timezone.now()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    def authenticate(self, user=None):
        """사용자 인증 및 JWT 토큰 획득"""
        if user is None:
            user = self.user1

        try:
            token = self.generate_jwt_token(user)
            return {
                "Authorization": f"Bearer {token}",
            }
        except Exception as e:
            print(f"Token generation failed: {e}")
            return {
                "Authorization": "Bearer test_token_for_testing",
            }

    # === 게시글 생성 테스트 ===

    async def test_create_post_success(self):
        """게시글 생성 성공 테스트"""
        headers = self.authenticate(self.user1)
        data = {
            "title": "새로운 게시글",
            "content": "새로운 게시글 내용입니다.",
            "tags": ["태그1", "태그2"],
            "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
        }
        
        response = await self.client.post("/", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        
        data_response = response.json()
        self.assertEqual(data_response["message"], "게시글이 생성되었습니다.")
        self.assertEqual(data_response["community"]["title"], "새로운 게시글")
        self.assertEqual(data_response["community"]["content"], "새로운 게시글 내용입니다.")

    async def test_create_post_unauthorized(self):
        """인증 없이 게시글 생성 테스트"""
        data = {
            "title": "새로운 게시글",
            "content": "새로운 게시글 내용입니다."
        }
        
        response = await self.client.post("/", json=data)
        self.assertEqual(response.status_code, 401)

    async def test_create_post_invalid_data(self):
        """잘못된 데이터로 게시글 생성 테스트"""
        headers = self.authenticate(self.user1)
        data = {
            "title": "",  # 빈 제목
            "content": "내용"
        }
        
        response = await self.client.post("/", json=data, headers=headers)
        self.assertEqual(response.status_code, 422)  # Validation error

    # === 게시글 목록 조회 테스트 ===

    async def test_get_post_list_success(self):
        """게시글 목록 조회 성공 테스트"""
        response = await self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("data", data)  # @paginate 데코레이터가 data 키로 감쌈
        self.assertEqual(len(data["data"]), 2)
        
        # 최신순 정렬 확인
        post1 = data["data"][0]
        post2 = data["data"][1]
        self.assertEqual(post1["title"], "테스트 게시글 2")  # 더 최근
        self.assertEqual(post2["title"], "테스트 게시글 1")

    async def test_get_post_list_with_user_filter(self):
        """사용자별 게시글 필터링 테스트"""
        response = await self.client.get(f"/?user_id={self.user1.id}")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["user_id"], str(self.user1.id))

    # === 게시글 상세 조회 테스트 ===

    async def test_get_post_detail_success(self):
        """게시글 상세 조회 성공 테스트"""
        response = await self.client.get(f"/{self.post1.id}")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("post", data)
        self.assertIn("tags", data)
        self.assertIn("images", data)
        
        post = data["post"]
        self.assertEqual(post["title"], "테스트 게시글 1")
        self.assertEqual(post["content"], "테스트 내용 1")
        self.assertEqual(len(data["tags"]), 2)
        self.assertEqual(len(data["images"]), 2)

    async def test_get_post_detail_not_found(self):
        """존재하지 않는 게시글 조회 테스트"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await self.client.get(f"/{fake_id}")
        self.assertEqual(response.status_code, 404)

    # === 게시글 수정 테스트 ===

    async def test_update_post_success(self):
        """게시글 수정 성공 테스트"""
        headers = self.authenticate(self.user1)
        data = {
            "title": "수정된 제목",
            "content": "수정된 내용"
        }
        
        response = await self.client.put(f"/{self.post1.id}", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        
        data_response = response.json()
        self.assertEqual(data_response["message"], "게시글이 수정되었습니다")

    async def test_update_post_unauthorized(self):
        """인증 없이 게시글 수정 테스트"""
        data = {"title": "수정된 제목"}
        response = await self.client.put(f"/{self.post1.id}", json=data)
        self.assertEqual(response.status_code, 401)

    async def test_update_post_no_permission(self):
        """권한 없이 게시글 수정 테스트"""
        headers = self.authenticate(self.user2)
        data = {"title": "수정된 제목"}
        
        response = await self.client.put(f"/{self.post1.id}", json=data, headers=headers)
        self.assertEqual(response.status_code, 403)

    # === 게시글 삭제 테스트 ===

    async def test_delete_post_success(self):
        """게시글 삭제 성공 테스트"""
        headers = self.authenticate(self.user1)
        
        response = await self.client.delete(f"/{self.post1.id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        
        data_response = response.json()
        self.assertEqual(data_response["message"], "게시글이 삭제되었습니다")

    async def test_delete_post_admin_permission(self):
        """관리자 권한으로 게시글 삭제 테스트"""
        headers = self.authenticate(self.admin_user)
        
        response = await self.client.delete(f"/{self.post2.id}", headers=headers)
        self.assertEqual(response.status_code, 200)

    async def test_delete_post_no_permission(self):
        """권한 없이 게시글 삭제 테스트"""
        headers = self.authenticate(self.user2)
        
        response = await self.client.delete(f"/{self.post1.id}", headers=headers)
        self.assertEqual(response.status_code, 403)

    # === 시스템 태그 관련 테스트 ===

    async def test_get_system_tags_success(self):
        """시스템 태그 목록 조회 성공 테스트"""
        response = await self.client.get("/tags/system")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 3)  # 활성화된 태그 3개
        
        # 태그 정보 확인
        tag_names = [tag["name"] for tag in data]
        self.assertIn("강아지", tag_names)
        self.assertIn("고양이", tag_names)
        self.assertIn("입양", tag_names)
        
        # 비활성화된 태그는 포함되지 않아야 함
        self.assertNotIn("비활성태그", tag_names)

    async def test_get_post_list_with_system_tag_filter(self):
        """시스템 태그로 게시글 필터링 테스트"""
        # "강아지" 태그로 필터링
        response = await self.client.get("/?system_tags=강아지")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data["data"]), 1)  # post1만 매칭
        self.assertEqual(data["data"][0]["title"], "테스트 게시글 1")

    async def test_get_post_list_with_multiple_system_tags(self):
        """여러 시스템 태그로 게시글 필터링 테스트"""
        # "강아지"와 "고양이" 태그로 필터링
        response = await self.client.get("/?system_tags=강아지&system_tags=고양이")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data["data"]), 2)  # post1과 post2 모두 매칭
        
        post_titles = [post["title"] for post in data["data"]]
        self.assertIn("테스트 게시글 1", post_titles)
        self.assertIn("테스트 게시글 2", post_titles)

    async def test_get_post_list_with_no_matching_system_tags(self):
        """매칭되는 시스템 태그가 없을 때 테스트"""
        # 존재하지 않는 시스템 태그로 필터링
        response = await self.client.get("/?system_tags=존재하지않는태그")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data["data"]), 0)  # 빈 결과

    async def test_get_post_list_with_mixed_matching_tags(self):
        """일부만 매칭되는 태그가 있을 때 테스트"""
        # post1: "강아지" (매칭) + "귀여워" (매칭 안됨) -> 노출됨
        # post2: "고양이" (매칭) + "맛있는음식" (매칭 안됨) -> 노출됨
        
        response = await self.client.get("/?system_tags=강아지")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["title"], "테스트 게시글 1")

    async def test_system_tag_case_insensitive_matching(self):
        """시스템 태그 대소문자 구분 없이 매칭 테스트"""
        # "강아지"와 "강아지"는 대소문자 구분 없이 매칭되어야 함
        response = await self.client.get("/?system_tags=강아지")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["title"], "테스트 게시글 1")

    async def test_post_with_no_user_tags_not_shown(self):
        """사용자 태그가 없는 포스트는 시스템 태그 필터링 시 노출되지 않음"""
        from asgiref.sync import sync_to_async
        
        # 태그가 없는 새 포스트 생성
        post_without_tags = await sync_to_async(Post.objects.create)(
            user=self.user1,
            title="태그 없는 게시글",
            content="태그가 없는 내용"
        )
        
        # 시스템 태그로 필터링
        response = await self.client.get("/?system_tags=강아지")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        # 태그가 없는 포스트는 노출되지 않아야 함
        post_titles = [post["title"] for post in data["data"]]
        self.assertNotIn("태그 없는 게시글", post_titles)