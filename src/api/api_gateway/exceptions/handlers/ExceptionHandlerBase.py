import logging
import traceback
from typing import Type

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.api_gateway.interfaces.ExceptionHandlerI import ExceptionHandlerI


class ExceptionHandlerBase(ExceptionHandlerI):
    @classmethod
    def handle (cls, request: Request, exception: Exception):
        raise NotImplementedError("This method should be overridden in subclasses")

    @staticmethod
    def handled_exception() -> Type[Exception]:
        raise NotImplementedError("This method should be overridden in subclasses")

    @staticmethod
    def invalid_exception_type(exception: Exception, expect_type: Type[Exception]):
        logging.error("ExceptionHandlerBase - check_exc_type - Expect to handle "
                      "{} but got {}".format(expect_type, type(exception)))
        return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "ExceptionHandlerBase - check_exc_type - Expect to handle "
                                   "{} but got {}".format(expect_type, type(exception))
                         }
        )


        
    
    