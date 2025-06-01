import json
from unittest.mock import MagicMock

import pytest
from starlette.responses import JSONResponse

from inputs.api_gateway.exceptions.handlers.UnauthorizedExceptionHandler import UnauthorizedExceptionHandler
from inputs.api_gateway.exceptions.models.UnauthorizedException import UnauthorizedException
from inputs.api_gateway.interfaces.ExceptionHandlerI import ExceptionHandlerI


class TestUnauthorizedExceptionHandler:
    @pytest.fixture
    def handler(self) -> UnauthorizedExceptionHandler:
        return UnauthorizedExceptionHandler()

    @pytest.fixture
    def request_obj(self):
        return MagicMock()

    @pytest.fixture
    def exception(self) -> UnauthorizedException:
        exception = MagicMock(spec=UnauthorizedException)
        return exception

    def test_init(self, handler):
        assert isinstance(handler, ExceptionHandlerI)
        assert isinstance(handler, UnauthorizedExceptionHandler)

    def test_handled_exception(self, handler):
        assert handler.handled_exception() == UnauthorizedException

    def test_handle(self, handler, exception, request_obj, mocker):
        logging_warning = mocker.patch("logging.warning")

        result = handler.handle(request_obj, exception)
        response_body = json.loads(result.body)

        assert isinstance(result, JSONResponse)
        assert result.status_code == 401
        assert response_body["detail"] is not None
        logging_warning.assert_called_once()
