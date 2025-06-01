import logging

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from inputs.api_gateway.exceptions.models.UnauthorizedException import UnauthorizedException
from inputs.api_gateway.interfaces.ExceptionHandlerI import ExceptionHandlerI


class UnauthorizedExceptionHandler(ExceptionHandlerI):
    @staticmethod
    def handled_exception() -> type[Exception]:
        return UnauthorizedException

    @classmethod
    def handle(cls, _: Request, exception: UnauthorizedException) -> JSONResponse:
        logging.warning("UnauthorizedException - %s", exception)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder({"detail": str(exception)}),
        )
