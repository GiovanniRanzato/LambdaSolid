from fastapi import APIRouter

from inputs.api.api_gateway.routes.default.v1 import health_check
from inputs.api.api_gateway.routes.default.v1 import sample

router = APIRouter()

router.include_router(health_check.router, prefix="/health_check", tags=["health_check"])
router.include_router(sample.router, prefix="/sample", tags=["sample"])
