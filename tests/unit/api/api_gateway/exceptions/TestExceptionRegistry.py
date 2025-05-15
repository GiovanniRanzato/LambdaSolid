import pytest
from api.api_gateway.exceptions.ExceptionsRegistry import ExceptionRegistry
from api.api_gateway.interfaces.ExceptionHandlerI import ExceptionHandlerI


class TestExceptionRegistry:
    @pytest.fixture
    def exception_registry(self):
        return ExceptionRegistry()

    def test_init(self, exception_registry):
        assert isinstance(exception_registry, ExceptionRegistry)

    def test_get_exceptions_handlers(self, exception_registry):
        registered_handlers =  exception_registry.exceptions_handlers()

        for registered_handler in registered_handlers:
            assert issubclass(registered_handler, ExceptionHandlerI)
