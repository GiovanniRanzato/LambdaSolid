from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse

from domain.models.ModelSample import ModelSample
from domain.services.ServiceSample import ServiceSample
from infrastructure import depends

router = APIRouter()


@router.post("/create", status_code=status.HTTP_200_OK)
async def create(
    sample: ModelSample, service_sample: ServiceSample = Depends(depends.get_service_sample)
) -> JSONResponse:
    created_sample = service_sample.create(sample)
    return JSONResponse(status_code=200, content=created_sample.model_dump_json())
