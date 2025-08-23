# LangSmith 연결 및 사용 가이드

## 개요
LangSmith는 LangChain 애플리케이션의 추적, 모니터링, 평가, 디버깅을 위한 개발자 플랫폼입니다. MPZ AI 추천 시스템과 연결하여 성능을 모니터링하고 개선할 수 있습니다.

## 1. LangSmith 계정 설정

### 1.1 계정 생성
1. https://smith.langchain.com 방문
2. 계정 생성 (GitHub/Google 연동 가능)
3. 조직/프로젝트 설정

### 1.2 API 키 생성
1. 대시보드에서 Settings → API Keys 선택
2. "Create API Key" 클릭
3. 키 이름 입력 (예: "MPZ-AI-Recommendation")
4. 생성된 API 키 복사

## 2. 환경 설정

### 2.1 환경변수 설정
`.env` 파일에 다음 설정 추가:

```bash
# LangSmith (LangChain 추적 및 모니터링)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="MPZ-AI-Recommendation"
LANGCHAIN_API_KEY="your_actual_api_key_here"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
```

### 2.2 Django 설정 확인
`cfehome/settings.py`에 LangSmith 설정이 추가되었는지 확인:

```python
# LangSmith Settings
LANGCHAIN_TRACING_V2 = config("LANGCHAIN_TRACING_V2", default=False, cast=bool)
LANGCHAIN_PROJECT = config("LANGCHAIN_PROJECT", default="MPZ-AI-Recommendation")
LANGCHAIN_API_KEY = config("LANGCHAIN_API_KEY", default="")
LANGCHAIN_ENDPOINT = config("LANGCHAIN_ENDPOINT", default="https://api.smith.langchain.com")
```

## 3. 사용 방법

### 3.1 LangSmith 관리 도구 실행
```bash
cd /Users/eomseongmin/mpz_fullstack/backend
source .venv/bin/activate
python langsmith_manager.py
```

### 3.2 초기 설정
1. LangSmith 관리 도구에서 "1. 초기 설정" 선택
2. 연결 테스트 및 프로젝트 생성
3. 테스트 데이터셋 생성

### 3.3 AI 추천 시스템 실행
서버 실행 시 자동으로 LangSmith 추적이 시작됩니다:

```bash
python manage.py runserver
```

AI 추천 API 호출 시 모든 실행이 LangSmith에 기록됩니다.

## 4. 모니터링 및 분석

### 4.1 실시간 모니터링
- LangSmith 대시보드에서 실시간 실행 상황 확인
- 각 요청의 상세 정보 (입력, 출력, 실행 시간, 토큰 사용량 등)

### 4.2 성능 분석
```bash
python langsmith_manager.py
# 메뉴에서 "5. 성능 분석" 선택
```

제공되는 메트릭:
- 총 실행 수
- 성공률
- 평균 실행 시간
- 실행 타입별 통계
- 일별 실행 수

### 4.3 데이터 내보내기
```bash
python langsmith_manager.py
# 메뉴에서 "6. 실행 기록 JSON 내보내기" 선택
```

## 5. 주요 기능

### 5.1 자동 추적
- 모든 AI 추천 요청이 자동으로 추적됩니다
- 입력 데이터, 출력 결과, 실행 시간, 에러 정보 기록
- LangChain/LangGraph의 모든 단계가 세부적으로 추적

### 5.2 디버깅
- 실패한 요청의 상세 에러 정보
- 각 단계별 실행 상황 확인
- 프롬프트와 모델 응답 분석

### 5.3 성능 최적화
- 느린 요청 식별
- 토큰 사용량 분석
- 비용 모니터링

### 5.4 A/B 테스트 지원
- 다양한 프롬프트나 모델 성능 비교
- 실험 결과 추적 및 분석

## 6. 대시보드 활용

### 6.1 주요 섹션
- **Traces**: 개별 실행 추적
- **Datasets**: 테스트 데이터셋 관리
- **Experiments**: A/B 테스트 및 실험
- **Analytics**: 성능 분석 및 통계

### 6.2 필터 및 검색
- 시간 범위별 필터링
- 상태별 필터링 (성공/실패)
- 사용자별 필터링
- 키워드 검색

## 7. 문제 해결

### 7.1 연결 문제
```bash
# 연결 테스트
python langsmith_manager.py
# 메뉴에서 "2. 연결 테스트" 선택
```

일반적인 문제:
- API 키 오류: .env 파일의 LANGCHAIN_API_KEY 확인
- 네트워크 문제: 방화벽 설정 확인
- 프로젝트 권한: LangSmith 대시보드에서 권한 확인

### 7.2 추적 안됨
1. 환경변수 확인: LANGCHAIN_TRACING_V2=true
2. 서버 재시작: 환경변수 변경 후 재시작 필요
3. API 키 유효성: 만료되지 않았는지 확인

### 7.3 성능 이슈
- 대량의 요청 시 추적 오버헤드 고려
- 필요시 LANGCHAIN_TRACING_V2=false로 비활성화 가능
- 샘플링 설정으로 일부만 추적 가능

## 8. 모범 사례

### 8.1 프로젝트 관리
- 환경별 프로젝트 분리 (development, staging, production)
- 의미있는 실행 이름 사용
- 메타데이터 활용으로 컨텍스트 정보 추가

### 8.2 모니터링
- 정기적인 성능 분석 (주/월별)
- 실패율 모니터링 및 알람 설정
- 사용량 추이 분석

### 8.3 개선
- 느린 요청 원인 분석 및 최적화
- 사용자 피드백과 추적 데이터 연관 분석
- 모델 성능 변화 추적

## 9. 추가 리소스

### 9.1 공식 문서
- [LangSmith 문서](https://docs.smith.langchain.com/)
- [LangChain 통합 가이드](https://docs.langchain.com/langsmith/)

### 9.2 커뮤니티
- [LangChain Discord](https://discord.gg/langchain)
- [GitHub Issues](https://github.com/langchain-ai/langsmith-sdk)

### 9.3 예제
- [LangSmith Cookbook](https://github.com/langchain-ai/langsmith-cookbook)
- [Best Practices](https://docs.smith.langchain.com/best-practices)

## 10. 보안 고려사항

### 10.1 개인정보 보호
- 사용자 개인정보는 추적에서 제외
- 민감한 데이터는 마스킹 처리
- GDPR/개인정보보호법 준수

### 10.2 API 키 관리
- .env 파일을 버전 관리에서 제외
- 운영 환경에서는 별도 키 사용
- 정기적인 키 로테이션

---

이 가이드를 따라 LangSmith를 설정하면 MPZ AI 추천 시스템의 성능을 체계적으로 모니터링하고 개선할 수 있습니다.
