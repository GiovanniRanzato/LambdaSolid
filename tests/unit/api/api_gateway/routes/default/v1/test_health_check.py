import pytest
from inputs.api_gateway.routes.default.v1.health_check import health_check


class TestHealthCheck:
    @pytest.mark.asyncio
    async def test_it_should_health_check(self):
        result = await health_check()
        assert result.status_code == 200
