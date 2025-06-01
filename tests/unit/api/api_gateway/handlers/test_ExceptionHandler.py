import json
from unittest.mock import MagicMock

import pytest
from starlette.responses import JSONResponse

from inputs.api.api_gateway.exceptions.handlers.ExceptionHandler import ExceptionHandler
from inputs.api.api_gateway.interfaces.ExceptionHandlerI import ExceptionHandlerI


class TestExceptionHandlerBase:
    @pytest.fixture
    def handler(self) -> ExceptionHandler:
        return ExceptionHandler()

    @pytest.fixture
    def request_obj(self):
        return MagicMock()

    @pytest.fixture
    def exception(self) -> Exception:
        return MagicMock(spec=Exception)

    def test_init(self, handler):
        assert isinstance(handler, ExceptionHandlerI)
        assert isinstance(handler, ExceptionHandler)

    def test_handled_exception(self, handler):
        assert handler.handled_exception() is Exception

    def test_handle(self, handler, exception, request_obj, mocker):
        logging_error = mocker.patch("logging.error")

        result = handler.handle(request_obj, exception)
        response_body = json.loads(result.body)

        assert isinstance(result, JSONResponse)
        assert result.status_code == 500
        assert response_body["detail"] is not None
        assert logging_error.call_count == 2
