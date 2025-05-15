import pytest

from infrastructure.config.SecretManager import SecretManager


class TestSecretManager:
    @pytest.fixture
    def secret_manager(self, mocker) -> SecretManager:
        mocker.patch("boto3.session.Session.client", return_value=mocker.Mock())
        return SecretManager(
            secret_name="test-secret-name", secret_region="some-region-2", secret_endpoint="http://localhost:8000"
        )

    def test_get_secrets(self, secret_manager, mocker):
        # Mock the response from the client
        mock_response = {"SecretString": '{"key": "value"}'}
        secret_manager.client.get_secret_value.return_value = mock_response

        # Call the method
        result = secret_manager.get_secrets()

        # Assertions
        assert result == {"key": "value"}
        secret_manager.client.get_secret_value.assert_called_once_with(SecretId=secret_manager.secret_name)
