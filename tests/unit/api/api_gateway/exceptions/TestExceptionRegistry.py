import pytest
from api.api_gateway.exceptions.ExceptionsRegistry import ExceptionRegistry
from api.api_gateway.exceptions.handlers.ExceptionHandler import ExceptionHandler
from api.api_gateway.exceptions.handlers.UnauthorizedExceptionHandler import UnauthorizedExceptionHandler
from api.api_gateway.exceptions.handlers.ValidationExceptionHandler import ValidationExceptionHandler


class TestExceptionRegistry:
    @pytest.fixture
    def exception_registry(self):
        return ExceptionRegistry()

    def test_init(self, exception_registry):
        assert isinstance(exception_registry, ExceptionRegistry)

    def test_get_exceptions_handlers(self, exception_registry):
        assert exception_registry.exceptions_handlers() == [
            ExceptionHandler,
            ValidationExceptionHandler,
            UnauthorizedExceptionHandler
        ]