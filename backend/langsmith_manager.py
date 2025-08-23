#!/usr/bin/env python
"""
LangSmith 관리 도구
- 프로젝트 생성 및 관리
- 추적 데이터 분석
- 성능 모니터링
- 실험 관리
"""
import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

# Django 프로젝트 설정
import django
sys.path.append('/Users/eomseongmin/mpz_fullstack/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')
django.setup()

from django.conf import settings

# LangSmith 클라이언트 임포트
try:
    from langsmith import Client
    from langsmith.schemas import Run, Example
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    print("⚠️ LangSmith가 설치되지 않았습니다. pip install langsmith를 실행하세요.")

class LangSmithManager:
    def __init__(self):
        if not LANGSMITH_AVAILABLE:
            raise ImportError("LangSmith 패키지가 필요합니다.")
        
        # 환경변수에서 API 키 확인
        self.api_key = getattr(settings, 'LANGCHAIN_API_KEY', '')
        self.project_name = getattr(settings, 'LANGCHAIN_PROJECT', 'MPZ-AI-Recommendation')
        self.endpoint = getattr(settings, 'LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')
        
        if not self.api_key:
            print("❌ LANGCHAIN_API_KEY가 설정되지 않았습니다.")
            print("LangSmith 계정을 만들고 API 키를 설정해주세요:")
            print("1. https://smith.langchain.com에서 계정 생성")
            print("2. API 키 생성")
            print("3. .env 파일의 LANGCHAIN_API_KEY에 추가")
            return
        
        try:
            self.client = Client(
                api_key=self.api_key,
                api_url=self.endpoint
            )
            print(f"✅ LangSmith 클라이언트 초기화 완료 (프로젝트: {self.project_name})")
        except Exception as e:
            print(f"❌ LangSmith 클라이언트 초기화 실패: {str(e)}")
            self.client = None
    
    def test_connection(self) -> bool:
        """LangSmith 연결 테스트"""
        if not self.client:
            return False
        
        try:
            # 프로젝트 목록 조회로 연결 테스트
            projects = list(self.client.list_projects(limit=1))
            print("✅ LangSmith 연결 성공!")
            return True
        except Exception as e:
            print(f"❌ LangSmith 연결 실패: {str(e)}")
            return False
    
    def create_project(self, project_name: str = None, description: str = None) -> bool:
        """새 프로젝트 생성"""
        if not self.client:
            return False
        
        if not project_name:
            project_name = self.project_name
        
        if not description:
            description = f"MPZ AI 추천 시스템 추적 프로젝트 - {datetime.now().strftime('%Y-%m-%d')}"
        
        try:
            project = self.client.create_project(
                project_name=project_name,
                description=description
            )
            print(f"✅ 프로젝트 '{project_name}' 생성 완료")
            return True
        except Exception as e:
            if "already exists" in str(e):
                print(f"📋 프로젝트 '{project_name}'는 이미 존재합니다")
                return True
            else:
                print(f"❌ 프로젝트 생성 실패: {str(e)}")
                return False
    
    def list_projects(self) -> List[Dict]:
        """프로젝트 목록 조회"""
        if not self.client:
            return []
        
        try:
            projects = list(self.client.list_projects())
            print(f"📋 총 {len(projects)}개의 프로젝트:")
            for project in projects:
                print(f"  - {project.name}: {project.description or '설명 없음'}")
            return [{"name": p.name, "description": p.description} for p in projects]
        except Exception as e:
            print(f"❌ 프로젝트 목록 조회 실패: {str(e)}")
            return []
    
    def get_recent_runs(self, days: int = 7, limit: int = 50) -> List[Dict]:
        """최근 실행 목록 조회"""
        if not self.client:
            return []
        
        try:
            start_time = datetime.now() - timedelta(days=days)
            runs = list(self.client.list_runs(
                project_name=self.project_name,
                start_time=start_time,
                limit=limit
            ))
            
            print(f"📊 최근 {days}일간 {len(runs)}개의 실행 기록:")
            
            run_data = []
            for run in runs:
                run_info = {
                    "id": str(run.id),
                    "name": run.name,
                    "run_type": run.run_type,
                    "start_time": run.start_time.isoformat() if run.start_time else None,
                    "end_time": run.end_time.isoformat() if run.end_time else None,
                    "status": run.status,
                    "error": run.error if hasattr(run, 'error') else None,
                    "inputs": run.inputs,
                    "outputs": run.outputs
                }
                run_data.append(run_info)
                
                # 간단한 요약 출력
                duration = ""
                if run.start_time and run.end_time:
                    duration = f"({(run.end_time - run.start_time).total_seconds():.2f}s)"
                
                print(f"  - {run.name} [{run.run_type}] {run.status} {duration}")
            
            return run_data
        except Exception as e:
            print(f"❌ 실행 기록 조회 실패: {str(e)}")
            return []
    
    def create_dataset(self, dataset_name: str, examples: List[Dict]) -> bool:
        """테스트 데이터셋 생성"""
        if not self.client:
            return False
        
        try:
            # 데이터셋 생성
            dataset = self.client.create_dataset(
                dataset_name=dataset_name,
                description=f"MPZ AI 추천 테스트 데이터셋 - {datetime.now().strftime('%Y-%m-%d')}"
            )
            
            # 예제 추가
            for example in examples:
                self.client.create_example(
                    dataset_id=dataset.id,
                    inputs=example.get("inputs", {}),
                    outputs=example.get("outputs", {})
                )
            
            print(f"✅ 데이터셋 '{dataset_name}' 생성 완료 ({len(examples)}개 예제)")
            return True
        except Exception as e:
            print(f"❌ 데이터셋 생성 실패: {str(e)}")
            return False
    
    def analyze_performance(self, days: int = 7) -> Dict[str, Any]:
        """성능 분석 리포트"""
        if not self.client:
            return {}
        
        try:
            start_time = datetime.now() - timedelta(days=days)
            runs = list(self.client.list_runs(
                project_name=self.project_name,
                start_time=start_time,
                limit=1000
            ))
            
            if not runs:
                print("📊 분석할 실행 기록이 없습니다.")
                return {}
            
            # 성능 지표 계산
            total_runs = len(runs)
            successful_runs = [r for r in runs if r.status == "success"]
            failed_runs = [r for r in runs if r.status == "error"]
            
            # 실행 시간 분석
            durations = []
            for run in successful_runs:
                if run.start_time and run.end_time:
                    duration = (run.end_time - run.start_time).total_seconds()
                    durations.append(duration)
            
            avg_duration = sum(durations) / len(durations) if durations else 0
            
            # 실행 타입별 분석
            run_types = {}
            for run in runs:
                run_type = run.run_type
                if run_type not in run_types:
                    run_types[run_type] = {"total": 0, "success": 0, "error": 0}
                
                run_types[run_type]["total"] += 1
                if run.status == "success":
                    run_types[run_type]["success"] += 1
                elif run.status == "error":
                    run_types[run_type]["error"] += 1
            
            report = {
                "period_days": days,
                "total_runs": total_runs,
                "success_rate": len(successful_runs) / total_runs if total_runs > 0 else 0,
                "average_duration_seconds": avg_duration,
                "run_types": run_types,
                "daily_counts": self._calculate_daily_counts(runs)
            }
            
            # 리포트 출력
            print(f"\\n📊 성능 분석 리포트 (최근 {days}일)")
            print("="*50)
            print(f"총 실행 수: {total_runs}")
            print(f"성공률: {report['success_rate']:.1%}")
            print(f"평균 실행 시간: {avg_duration:.2f}초")
            print(f"실패한 실행: {len(failed_runs)}개")
            
            print("\\n📈 실행 타입별 통계:")
            for run_type, stats in run_types.items():
                success_rate = stats["success"] / stats["total"] if stats["total"] > 0 else 0
                print(f"  - {run_type}: {stats['total']}회 (성공률: {success_rate:.1%})")
            
            return report
            
        except Exception as e:
            print(f"❌ 성능 분석 실패: {str(e)}")
            return {}
    
    def _calculate_daily_counts(self, runs: List) -> Dict[str, int]:
        """일별 실행 수 계산"""
        daily_counts = {}
        for run in runs:
            if run.start_time:
                date_str = run.start_time.strftime('%Y-%m-%d')
                daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        return daily_counts
    
    def export_runs_to_json(self, filepath: str, days: int = 7) -> bool:
        """실행 기록을 JSON으로 내보내기"""
        runs_data = self.get_recent_runs(days=days, limit=1000)
        
        if not runs_data:
            print("내보낼 데이터가 없습니다.")
            return False
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(runs_data, f, ensure_ascii=False, indent=2)
            print(f"✅ 실행 기록을 {filepath}에 저장했습니다.")
            return True
        except Exception as e:
            print(f"❌ JSON 내보내기 실패: {str(e)}")
            return False
    
    def setup_langsmith_for_ai_system(self):
        """AI 추천 시스템을 위한 LangSmith 초기 설정"""
        print("🚀 MPZ AI 추천 시스템을 위한 LangSmith 설정 시작")
        print("="*50)
        
        # 1. 연결 테스트
        if not self.test_connection():
            return False
        
        # 2. 프로젝트 생성
        if not self.create_project():
            return False
        
        # 3. 테스트 데이터셋 생성
        sample_examples = [
            {
                "inputs": {
                    "user_preferences": {
                        "personality_type": "활발한_타입",
                        "activity_preference": 4,
                        "home_type": "아파트"
                    },
                    "request_type": "recommendation"
                },
                "outputs": {
                    "recommended_animals": ["골든 리트리버", "비글", "보더 콜리"],
                    "matching_reasons": ["높은 활동성", "친화적 성격", "훈련 용이성"]
                }
            },
            {
                "inputs": {
                    "user_preferences": {
                        "personality_type": "차분한_타입",
                        "activity_preference": 2,
                        "home_type": "단독주택"
                    },
                    "request_type": "recommendation"
                },
                "outputs": {
                    "recommended_animals": ["페르시안 고양이", "래그돌", "브리티시 숏헤어"],
                    "matching_reasons": ["낮은 활동성", "온순한 성격", "독립적 특성"]
                }
            }
        ]
        
        dataset_name = f"mpz-ai-recommendations-{datetime.now().strftime('%Y%m%d')}"
        self.create_dataset(dataset_name, sample_examples)
        
        print("\\n✅ LangSmith 설정 완료!")
        print("\\n📋 다음 단계:")
        print("1. AI 추천 시스템 실행 시 자동으로 추적됩니다")
        print("2. https://smith.langchain.com에서 대시보드 확인")
        print("3. 성능 모니터링 및 디버깅 활용")
        
        return True

def main():
    """메인 실행 함수"""
    print("🔧 LangSmith 관리 도구")
    print("="*30)
    
    try:
        manager = LangSmithManager()
        
        if not manager.client:
            print("\\n❌ LangSmith 클라이언트 초기화 실패")
            print("\\n🔧 설정 방법:")
            print("1. https://smith.langchain.com에서 계정 생성")
            print("2. API 키 생성")
            print("3. .env 파일에 LANGCHAIN_API_KEY 추가")
            print('   LANGCHAIN_API_KEY="your_api_key_here"')
            print("4. 서버 재시작")
            return
        
        while True:
            print("\\n🎯 작업을 선택하세요:")
            print("1. 초기 설정 (프로젝트 생성 등)")
            print("2. 연결 테스트")
            print("3. 프로젝트 목록 조회")
            print("4. 최근 실행 기록 조회")
            print("5. 성능 분석")
            print("6. 실행 기록 JSON 내보내기")
            print("0. 종료")
            
            choice = input("\\n선택 (0-6): ").strip()
            
            if choice == "1":
                manager.setup_langsmith_for_ai_system()
            elif choice == "2":
                manager.test_connection()
            elif choice == "3":
                manager.list_projects()
            elif choice == "4":
                days = input("조회할 일수 (기본 7일): ").strip()
                days = int(days) if days.isdigit() else 7
                manager.get_recent_runs(days=days)
            elif choice == "5":
                days = input("분석할 일수 (기본 7일): ").strip()
                days = int(days) if days.isdigit() else 7
                manager.analyze_performance(days=days)
            elif choice == "6":
                filepath = input("저장할 파일 경로 (기본: langsmith_runs.json): ").strip()
                filepath = filepath or "langsmith_runs.json"
                days = input("내보낼 일수 (기본 7일): ").strip()
                days = int(days) if days.isdigit() else 7
                manager.export_runs_to_json(filepath, days)
            elif choice == "0":
                print("👋 종료합니다.")
                break
            else:
                print("❌ 잘못된 선택입니다.")
    
    except KeyboardInterrupt:
        print("\\n👋 사용자가 종료했습니다.")
    except Exception as e:
        print(f"\\n❌ 오류 발생: {str(e)}")

if __name__ == "__main__":
    main()
