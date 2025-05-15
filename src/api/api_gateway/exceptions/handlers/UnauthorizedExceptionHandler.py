import logging

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.api_gateway.exceptions.models.UnauthorizedException import UnauthorizedException
from api.api_gateway.exceptions.handlers.ExceptionHandlerBase import ExceptionHandlerBase


class UnauthorizedExceptionHandler(ExceptionHandlerBase):
    @staticmethod
    def handled_exception() -> type[Exception]:
        return UnauthorizedException

    @classmethod
    def handle(cls, _: Request, exception: UnauthorizedException) -> JSONResponse:
        if not isinstance(exception, cls.handled_exception()):
            return cls.invalid_exception_type(exception, cls.handled_exception())

        logging.warning("UnauthorizedException - %s", exception)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder({"detail": str(exception)}),
        )
