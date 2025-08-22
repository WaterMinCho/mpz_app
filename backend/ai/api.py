from ninja import Router, Schema, Field
from ninja.errors import HttpError
from typing import List, Dict, Any, Optional
from django.http import HttpRequest
from asgiref.sync import sync_to_async
import uuid
import json
from datetime import datetime
from langchain_core.output_parsers import PydanticOutputParser

from api.security import jwt_auth
from ai.agents import get_animal_matching_agent
from ai.schemas import AIAnimalMatchingResponse
from ai.prompts import SIMPLE_RECOMMENDATION_PROMPT, TOOL_TEST_PROMPT
from ai.tools import (
    get_user_personality_test_data,
    get_available_animals,
    filter_animals_by_characteristics
)

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
        
        # 응답 구성
        response_data = {
            "success": True,
            "data": ai_result,
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
