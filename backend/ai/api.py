from ninja import Router, Schema, Field
from ninja.errors import HttpError
from typing import List, Dict, Any, Optional
from django.http import HttpRequest
from asgiref.sync import sync_to_async
import uuid
from datetime import datetime
from langchain_core.output_parsers import PydanticOutputParser

from api.security import jwt_auth
from ai.agents import get_animal_matching_agent
from ai.schemas import AIAnimalMatchingResponse
from ai.prompts import SIMPLE_RECOMMENDATION_PROMPT, TOOL_TEST_PROMPT
from ai.tools import (
    get_user_personality_test_data,
    get_available_animals,
)
from favorites.models import PersonalityTest

router = Router(tags=["AI_Animal_Matching"])


class AnimalRecommendationRequest(Schema):
    """동물 추천 요청 스키마"""
    user_id: Optional[str] = Field(None, description="사용자 ID (없으면 현재 로그인 사용자 사용)")
    preferences: Optional[Dict[str, Any]] = Field(None, description="추가 선호사항")
    limit: Optional[int] = Field(5, description="추천받을 동물 수 (기본값: 5)")


class AnimalRecommendationResponse(Schema):
    """동물 추천 응답 스키마"""
    success: bool = Field(..., description="성공 여부")
    data: Dict[str, Any] = Field(..., description="AI 매칭 결과 (구조화된 응답)")
    meta: Dict[str, Any] = Field(..., description="메타 정보")


class PersonalityTestAnswer(Schema):
    """성격 테스트 개별 질문 응답"""
    question_id: str = Field(..., description="질문 ID")
    question_text: str = Field(..., description="질문 내용")
    answer: str = Field(..., description="사용자 응답")
    answer_type: str = Field(..., description="응답 타입 (text, choice, scale 등)")


class PersonalityTestSubmission(Schema):
    """성격 테스트 제출 데이터"""
    test_name: str = Field(..., description="테스트 이름")
    test_version: Optional[str] = Field("v1.0", description="테스트 버전")
    answers: List[PersonalityTestAnswer] = Field(..., description="질문-응답 목록")
    additional_notes: Optional[str] = Field(None, description="추가 메모")
    test_duration_minutes: Optional[int] = Field(None, description="테스트 소요 시간(분)")


class PersonalityTestResponse(Schema):
    """성격 테스트 저장 응답"""
    success: bool = Field(..., description="성공 여부")
    test_id: str = Field(..., description="저장된 테스트 ID")
    message: str = Field(..., description="응답 메시지")
    saved_at: str = Field(..., description="저장 시간")


@router.post(
    "/recommend",
    summary="[AI] 동물 추천",
    description="사용자의 성격 테스트 결과를 기반으로 적합한 동물을 AI가 추천합니다.",
    response={
        200: AnimalRecommendationResponse,
        400: dict,
        401: dict,
        404: dict,
        500: dict,
    },
    auth=jwt_auth,
)
async def recommend_animals(request: HttpRequest, data: AnimalRecommendationRequest):
    """AI 기반 동물 추천 API - 에이전트 직접 활용"""
    try:
        current_user = request.auth
        target_user_id = data.user_id if data.user_id else str(current_user.id)
        
        # 권한 체크: 자신의 추천만 받을 수 있음 (일반 사용자의 경우)
        if current_user.user_type == "일반사용자" and target_user_id != str(current_user.id):
            raise HttpError(403, "자신의 동물 추천만 받을 수 있습니다")
        
        @sync_to_async
        def run_agent_recommendation():
            """에이전트를 사용한 AI 추천 실행"""
            try:
                # AI 에이전트 생성
                agent = get_animal_matching_agent()
                
                # 대화 세션 ID 생성
                thread_id = str(uuid.uuid4())
                
                # 에이전트에게 직접 추천 요청
                user_query = SIMPLE_RECOMMENDATION_PROMPT.format(
                    user_id=target_user_id,
                    limit=data.limit,
                    preferences=data.preferences if data.preferences else '없음'
                )
                
                # AI 에이전트 실행
                result = agent.invoke(
                    {"messages": [("user", user_query)]},
                    config={"configurable": {"thread_id": thread_id}}
                )
                
                # 응답에서 JSON 구조 추출 시도
                ai_response = result["messages"][-1].content
                
                # Pydantic Parser로 구조화된 응답 파싱 시도
                parser = PydanticOutputParser(pydantic_object=AIAnimalMatchingResponse)
                
                try:
                    # JSON 부분만 추출하여 파싱
                    import re
                    json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
                    if json_match:
                        json_str = json_match.group()
                        parsed_response = parser.parse(json_str)
                        return parsed_response.dict()
                    else:
                        # JSON 형태가 아닌 경우 raw 응답 반환
                        return {
                            "raw_response": ai_response,
                            "parsing_status": "failed - no JSON found"
                        }
                except Exception as parse_error:
                    # 파싱 실패 시 raw 응답 반환
                    return {
                        "raw_response": ai_response,
                        "parsing_status": f"failed - {str(parse_error)}"
                    }
                
            except Exception as e:
                return {
                    "error": f"에이전트 실행 중 오류: {str(e)}",
                    "status": "agent_error"
                }
        
        # AI 추천 실행
        ai_result = await run_agent_recommendation()
        
        # 추천 결과를 PersonalityTest의 result 필드에 저장
        @sync_to_async
        def save_recommendation_result():
            try:
                # 해당 사용자의 가장 최근 PersonalityTest 가져오기
                latest_test = PersonalityTest.objects.filter(
                    user_id=target_user_id
                ).order_by('-completed_at').first()
                
                if latest_test:
                    # AI 추천 결과를 result 필드에 저장
                    recommendation_result = {
                        "ai_recommendation": ai_result,
                        "recommendation_date": datetime.now().isoformat(),
                        "model_used": "gpt-4o-mini",
                        "agent_used": "animal-matching-assistant",
                        "preferences": data.preferences,
                        "limit": data.limit
                    }
                    
                    latest_test.result = recommendation_result
                    latest_test.save()
                    
                    return {
                        "saved": True,
                        "personality_test_id": str(latest_test.id),
                        "message": "추천 결과가 성격 테스트 결과에 저장되었습니다."
                    }
                else:
                    return {
                        "saved": False,
                        "message": "해당 사용자의 성격 테스트를 찾을 수 없습니다."
                    }
                    
            except Exception as e:
                return {
                    "saved": False,
                    "error": f"결과 저장 중 오류: {str(e)}"
                }
        
        # 추천 결과 저장 실행
        save_result = await save_recommendation_result()
        
        # 응답 구성
        response_data = {
            "success": True,
            "data": ai_result,
            "save_status": save_result,
            "meta": {
                "user_id": target_user_id,
                "request_limit": data.limit,
                "preferences": data.preferences,
                "generated_at": datetime.now().isoformat(),
                "api_version": "v1.0",
                "model_used": "gpt-4o-mini",
                "agent_used": "animal-matching-assistant"
            }
        }
        
        return response_data
        
    except HttpError:
        raise
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"AI 동물 추천 중 오류: {str(e)}")
        raise HttpError(500, f"AI 추천 중 오류가 발생했습니다: {str(e)}")


@router.get(
    "/test-tools",
    summary="[AI] 도구 테스트",
    description="AI 도구들이 제대로 작동하는지 테스트합니다.",
    response={200: dict, 500: dict},
    auth=jwt_auth,
)
async def test_ai_tools(request: HttpRequest):
    """AI 도구 테스트 API - 에이전트 활용"""
    try:
        current_user = request.auth
        
        @sync_to_async  
        def test_with_agent():
            """에이전트를 사용한 도구 테스트"""
            results = {}
            
            try:
                # AI 에이전트 생성 테스트
                agent = get_animal_matching_agent()
                
                # 도구 테스트 프롬프트 실행
                test_query = TOOL_TEST_PROMPT.format(user_id=str(current_user.id))
                
                # 에이전트 실행
                thread_id = str(uuid.uuid4())
                result = agent.invoke(
                    {"messages": [("user", test_query)]},
                    config={"configurable": {"thread_id": thread_id}}
                )
                
                ai_response = result["messages"][-1].content
                
                results["agent_test"] = {
                    "success": True,
                    "response": ai_response,
                    "thread_id": thread_id
                }
                
            except Exception as e:
                results["agent_test"] = {"error": f"에이전트 테스트 실패: {str(e)}"}
            
            # 개별 도구 직접 테스트
            try:
                personality_result = get_user_personality_test_data.invoke({"user_id": str(current_user.id)})
                results["direct_personality_test"] = personality_result
            except Exception as e:
                results["direct_personality_test"] = {"error": str(e)}
            
            try:
                animals_result = get_available_animals.invoke({"limit": 2})
                results["direct_animals_test"] = {
                    "count": len(animals_result) if isinstance(animals_result, list) else 0,
                    "sample": animals_result[:1] if animals_result and isinstance(animals_result, list) else []
                }
            except Exception as e:
                results["direct_animals_test"] = {"error": str(e)}
            
            return results
        
        test_results = await test_with_agent()
        
        return {
            "status": "success",
            "message": "AI 도구 및 에이전트 테스트 완료",
            "results": test_results,
            "user_id": str(current_user.id),
            "test_time": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HttpError(500, f"도구 테스트 중 오류: {str(e)}")


@router.post(
    "/personality-test",
    summary="[AI] 성격 테스트 결과 저장",
    description="사용자의 성격 테스트 질문과 응답을 Q&A 조합으로 JSON 형태로 저장합니다.",
    response={
        200: PersonalityTestResponse,
        400: dict,
        401: dict,
        500: dict,
    },
    auth=jwt_auth,
)
async def save_personality_test(request: HttpRequest, data: PersonalityTestSubmission):
    """성격 테스트 결과 저장 API"""
    try:
        current_user = request.auth
        
        @sync_to_async
        def save_test_data():
            """성격 테스트 데이터를 데이터베이스에 저장"""
            try:
                # Q&A 조합을 JSON 형태로 구성
                qa_data = []
                for answer in data.answers:
                    qa_item = {
                        "question_id": answer.question_id,
                        "question": answer.question_text,
                        "answer": answer.answer,
                        "answer_type": answer.answer_type
                    }
                    qa_data.append(qa_item)
                
                # PersonalityTest 모델에 저장 (result는 비워둠)
                personality_test = PersonalityTest.objects.create(
                    user=current_user,
                    test_type=data.test_name,
                    answers=qa_data,  # answers 필드에만 Q&A 데이터 저장
                    # result는 None으로 비워둠 (AI 분석 후 별도로 저장)
                    completed_at=datetime.now()
                )
                
                return {
                    "success": True,
                    "test_id": str(personality_test.id),
                    "message": "성격 테스트 결과가 성공적으로 저장되었습니다.",
                    "saved_at": personality_test.completed_at.isoformat()
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "test_id": "",
                    "message": f"데이터 저장 중 오류가 발생했습니다: {str(e)}",
                    "saved_at": ""
                }
        
        # 성격 테스트 데이터 저장 실행
        save_result = await save_test_data()
        
        return PersonalityTestResponse(**save_result)
        
    except HttpError:
        raise
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"성격 테스트 저장 중 오류: {str(e)}")
        raise HttpError(500, f"성격 테스트 저장 중 오류가 발생했습니다: {str(e)}")


@router.get(
    "/personality-test/{test_id}",
    summary="[AI] 성격 테스트 결과 조회",
    description="저장된 성격 테스트 결과를 조회합니다.",
    response={
        200: dict,
        401: dict,
        404: dict,
        500: dict,
    },
    auth=jwt_auth,
)
async def get_personality_test(request: HttpRequest, test_id: str):
    """성격 테스트 결과 조회 API"""
    try:
        current_user = request.auth
        
        @sync_to_async
        def retrieve_test_data():
            """데이터베이스에서 성격 테스트 데이터 조회"""
            try:
                # UUID 형식 검증
                import uuid
                try:
                    uuid.UUID(test_id)
                except ValueError:
                    return {
                        "success": False,
                        "message": "해당 테스트를 찾을 수 없습니다."
                    }
                
                # 해당 테스트 데이터 조회
                personality_test = PersonalityTest.objects.get(id=test_id)
                
                # 권한 체크: 자신의 테스트만 조회 가능
                if str(personality_test.user.id) != str(current_user.id):
                    return {
                        "success": False,
                        "message": "해당 테스트에 대한 접근 권한이 없습니다."
                    }
                
                return {
                    "success": True,
                    "test_data": personality_test.answers,  # answers 필드 반환
                    "test_type": personality_test.test_type,
                    "completed_at": personality_test.completed_at.isoformat(),
                    "user_id": str(personality_test.user.id),
                    "result": personality_test.result  # AI 분석 결과 (있다면)
                }
                
            except PersonalityTest.DoesNotExist:
                return {
                    "success": False,
                    "message": "해당 테스트를 찾을 수 없습니다."
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"데이터 조회 중 오류가 발생했습니다: {str(e)}"
                }
        
        # 성격 테스트 데이터 조회 실행
        retrieve_result = await retrieve_test_data()
        
        if not retrieve_result["success"]:
            if "찾을 수 없습니다" in retrieve_result["message"]:
                raise HttpError(404, retrieve_result["message"])
            else:
                raise HttpError(500, retrieve_result["message"])
        
        return retrieve_result
        
    except HttpError:
        raise
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"성격 테스트 조회 중 오류: {str(e)}")
        raise HttpError(500, f"성격 테스트 조회 중 오류가 발생했습니다: {str(e)}")


@router.get(
    "/personality-test/user/{user_id}",
    summary="[AI] 사용자별 성격 테스트 목록 조회",
    description="특정 사용자의 모든 성격 테스트 목록을 조회합니다.",
    response={
        200: dict,
        401: dict,
        403: dict,
        500: dict,
    },
    auth=jwt_auth,
)
async def get_user_personality_tests(request: HttpRequest, user_id: str):
    """사용자별 성격 테스트 목록 조회 API"""
    try:
        current_user = request.auth
        
        # 권한 체크: 자신의 테스트만 조회 가능 (일반 사용자의 경우)
        if current_user.user_type == "일반사용자" and user_id != str(current_user.id):
            raise HttpError(403, "자신의 성격 테스트만 조회할 수 있습니다")
        
        @sync_to_async
        def retrieve_user_tests():
            """사용자의 모든 성격 테스트 데이터 조회"""
            try:
                # 해당 사용자의 모든 테스트 조회
                personality_tests = PersonalityTest.objects.filter(
                    user_id=user_id
                ).order_by('-completed_at')
                
                tests_list = []
                for test in personality_tests:
                    test_summary = {
                        "test_id": str(test.id),
                        "test_type": test.test_type,
                        "completed_at": test.completed_at.isoformat(),
                        "total_questions": len(test.answers) if test.answers else 0,
                        "test_name": test.test_type  # test_type이 test_name과 동일
                    }
                    tests_list.append(test_summary)
                
                return {
                    "success": True,
                    "user_id": user_id,
                    "total_tests": len(tests_list),
                    "tests": tests_list
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "message": f"데이터 조회 중 오류가 발생했습니다: {str(e)}"
                }
        
        # 사용자별 성격 테스트 데이터 조회 실행
        retrieve_result = await retrieve_user_tests()
        
        if not retrieve_result["success"]:
            raise HttpError(500, retrieve_result["message"])
        
        return retrieve_result
        
    except HttpError:
        raise
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"사용자별 성격 테스트 조회 중 오류: {str(e)}")
        raise HttpError(500, f"사용자별 성격 테스트 조회 중 오류가 발생했습니다: {str(e)}")
