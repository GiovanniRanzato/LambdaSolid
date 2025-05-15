from abc import ABC, abstractmethod
from typing import Type

from starlette.requests import Request


class ExceptionHandlerI(ABC):
    @staticmethod
    def handled_exception() -> Type[Exception]:
        """Return the exception type that this handler can handle"""

    @classmethod
    @abstractmethod
    def handle(cls, request: Request, exception: Exception) -> dict:
        """Handle the exception and return a response"""

