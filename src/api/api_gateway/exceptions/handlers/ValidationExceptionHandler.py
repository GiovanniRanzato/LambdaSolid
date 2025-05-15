import logging

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from api.api_gateway.interfaces.ExceptionHandlerI import ExceptionHandlerI


class ValidationExceptionHandler(ExceptionHandlerI):
    @staticmethod
    def handled_exception() -> type[Exception]:
        return RequestValidationError

    @classmethod
    def handle(cls, _: Request, exception: RequestValidationError) -> JSONResponse:
        logging.warning("RequestValidationError - %s", exception)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exception.errors(), "body": exception.body}),
        )
