from fastapi import APIRouter

from api.api_gateway.routes.default.v1 import health_check

router = APIRouter()

router.include_router(health_check.router, prefix="/health_check", tags=["health_check"])