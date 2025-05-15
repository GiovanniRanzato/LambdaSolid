from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from api.api_gateway.APIGatewayHandler import APIGatewayHandler
from api.api_gateway.interfaces.APIGatewayRequestI import APIGatewayRequestI

class TestApiGatewayHandler:
    @pytest.fixture
    def handler(self):
        return APIGatewayHandler()

    @pytest.fixture
    def event(self):
        event = MagicMock(spec=APIGatewayRequestI)
        event.get_version.return_value = "v1"
        event.get_stage.return_value = "default"
        event.get_body.return_value = {"key": "value"}
        event.get_context.return_value = {"key": "value"}
        return event

    def test_init(self, handler):
        assert isinstance(handler, APIGatewayHandler)

    def test_handle_standalone_returns_fastapi_app(self, handler, event):
        handler = APIGatewayHandler(standalone=True)
        app = handler.handle(event)

        assert isinstance(app, FastAPI)

    def test_handle_with_mangum(self, handler, event, mocker):
        mangum_mock = mocker.patch("api.api_gateway.APIGatewayHandler.Mangum")
        app_mock = mocker.MagicMock()
        mangum_mock.return_value = app_mock

        handler.handle(event)

        mangum_mock.assert_called_once()
        app_mock.assert_called_once_with(event.get_body(), event.get_context())


