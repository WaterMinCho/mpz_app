from langgraph.prebuilt import create_react_agent
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from django.conf import settings

from ai.llms import get_openai_model
from ai.tools import animal_matching_tools
from ai.schemas import AIAnimalMatchingResponse
from ai.prompts import ANIMAL_MATCHING_SYSTEM_PROMPT

# LangSmith 추적을 위한 메타데이터 추가
def add_langsmith_metadata(inputs: dict) -> dict:
    """LangSmith 추적을 위한 메타데이터 추가"""
    metadata = {
        "application": "MPZ-AI-Recommendation",
        "version": "1.0",
        "environment": "development" if settings.DEBUG else "production",
    }
    
    # 사용자 정보가 있다면 추가 (개인정보는 제외)
    if "user_id" in inputs:
        metadata["user_type"] = "registered"
    
    inputs["_metadata"] = metadata
    return inputs


def get_animal_matching_agent(model=None, checkpointer=None):
    """
    동물 매칭 에이전트를 생성합니다.
    사용자의 성격 테스트 결과를 기반으로 적합한 동물을 추천합니다.
    
    LangSmith 추적이 활성화되어 있으면 자동으로 추적됩니다.
    """
    llm_model = get_openai_model(model=model)
    
    # Pydantic Parser 설정
    parser = PydanticOutputParser(pydantic_object=AIAnimalMatchingResponse)
    format_instructions = parser.get_format_instructions()

    # 프롬프트에 format_instructions 추가
    system_prompt = ANIMAL_MATCHING_SYSTEM_PROMPT.format(format_instructions=format_instructions)

    agent = create_react_agent(
        model=llm_model,  
        tools=animal_matching_tools,  
        prompt=system_prompt,
        checkpointer=checkpointer,
        name="animal-matching-assistant"
    )
    
    # LangSmith 추적이 활성화된 경우 메타데이터 추가
    if getattr(settings, 'LANGCHAIN_TRACING_V2', False):
        agent = RunnableLambda(add_langsmith_metadata) | agent
        
    return agent
