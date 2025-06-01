import pytest

from inputs.api.api_gateway.exceptions.models.UnauthorizedException import UnauthorizedException


class TestUnauthorizedException:
    @pytest.fixture
    def exception_obj(self):
        return UnauthorizedException()

    def test_init(self, exception_obj):
        assert str(exception_obj) == "Unauthorized Exception"
        assert isinstance(exception_obj, UnauthorizedException)
