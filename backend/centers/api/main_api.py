from ninja import Router
from centers.api.contract_api import router as contract_router
from centers.api.procedure_api import router as procedure_router

# centers 앱의 메인 라우터
router = Router()

# 계약서 템플릿 관련 라우터 추가
router.add_router("/procedures/contract-template/", contract_router)

# 프로시저 설정 관련 라우터 추가
router.add_router("/procedures/settings/", procedure_router)
