from fastapi import APIRouter, status
from starlette.responses import Response


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check() -> Response:
    return Response(status_code=200, content="OK")
