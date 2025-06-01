import json
from unittest.mock import MagicMock

import pytest
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from inputs.api_gateway.exceptions.handlers.ValidationExceptionHandler import ValidationExceptionHandler
from inputs.api_gateway.interfaces.ExceptionHandlerI import ExceptionHandlerI


class TestValidationExceptionHandler:
    @pytest.fixture
    def handler(self) -> ValidationExceptionHandler:
        return ValidationExceptionHandler()

    @pytest.fixture
    def request_obj(self):
        return MagicMock()

    @pytest.fixture
    def exception(self) -> RequestValidationError:
        exception = MagicMock(spec=RequestValidationError)
        exception.errors.return_value = {"some_error": "some_description"}
        exception.body = "some other details"
        return exception

    def test_init(self, handler):
        assert isinstance(handler, ExceptionHandlerI)
        assert isinstance(handler, ValidationExceptionHandler)

    def test_handled_exception(self, handler):
        assert handler.handled_exception() == RequestValidationError

    def test_handle(self, handler, exception, request_obj, mocker):
        logging_warning = mocker.patch("logging.warning")

        result = handler.handle(request_obj, exception)
        response_body = json.loads(result.body)

        assert isinstance(result, JSONResponse)
        assert result.status_code == 422
        assert response_body["detail"] == exception.errors()
        assert response_body["body"] == exception.body
        logging_warning.assert_called_once()
