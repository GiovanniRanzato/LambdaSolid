import json
from unittest.mock import MagicMock

import pytest
from starlette.responses import JSONResponse

from api.api_gateway.exceptions.handlers.ExceptionHandlerBase import ExceptionHandlerBase
from api.api_gateway.interfaces.ExceptionHandlerI import ExceptionHandlerI

class TestExceptionHandlerBase:
    @pytest.fixture
    def handler(self) -> ExceptionHandlerBase:
        return ExceptionHandlerBase()

    def test_init(self, handler):
        assert isinstance(handler, ExceptionHandlerI)
        assert isinstance(handler, ExceptionHandlerBase)

    def test_invalid_exception_type(self, handler, mocker):
        unhandled_exception = MagicMock()
        expected_message = ("ExceptionHandlerBase - check_exc_type - Expect to handle "
                            "<class 'Exception'> but got <class 'unittest.mock.MagicMock'>")

        logging_error = mocker.patch("logging.error")
        result = handler.invalid_exception_type(unhandled_exception, Exception)


        assert isinstance(result, JSONResponse)
        assert json.loads(result.body)['detail'] == expected_message
        logging_error.assert_called_once_with(expected_message)


