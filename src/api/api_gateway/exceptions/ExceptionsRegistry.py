from typing import Type

from api.api_gateway.exceptions.handlers.ExceptionHandler import ExceptionHandler
from api.api_gateway.exceptions.handlers.UnauthorizedExceptionHandler import UnauthorizedExceptionHandler
from api.api_gateway.exceptions.handlers.ValidationExceptionHandler import ValidationExceptionHandler
from api.api_gateway.interfaces.ExceptionHandlerI import ExceptionHandlerI


class ExceptionRegistry:
    @staticmethod
    def exceptions_handlers() ->list[Type[ExceptionHandlerI]]:
        # Add custom exceptions and relative handlers here
        return [
            ExceptionHandler,
            ValidationExceptionHandler,
            UnauthorizedExceptionHandler,
        ]