import logging

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.api_gateway.exceptions.handlers.ExceptionHandlerBase import ExceptionHandlerBase

class ValidationExceptionHandler(ExceptionHandlerBase):
    @staticmethod
    def handled_exception() -> type[Exception]:
        return RequestValidationError

    @classmethod
    def handle(cls, _: Request, exception: RequestValidationError) -> JSONResponse:
        if not isinstance(exception, cls.handled_exception()):
            return cls.invalid_exception_type(exception, cls.handled_exception())

        logging.warning("RequestValidationError - %s", exception)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exception.errors(), "body": exception.body}),
        )