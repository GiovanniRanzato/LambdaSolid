import logging
import traceback
from typing import Type

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from inputs.api_gateway.interfaces.ExceptionHandlerI import ExceptionHandlerI


class ExceptionHandler(ExceptionHandlerI):
    @staticmethod
    def handled_exception() -> Type[Exception]:
        return Exception

    @classmethod
    def handle(cls, request: Request, exception: Exception):
        error_message = exception.args[0] if exception.args else str(exception)
        logging.error(traceback.format_exc())
        logging.error(error_message)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Something went wrong {error_message}"},
        )
