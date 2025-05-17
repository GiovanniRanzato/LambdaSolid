# tests/infrastructure/config/test_config.py
import os
from unittest.mock import patch, MagicMock

import pytest

from infrastructure.config.Config import Config


class TestConfig:
    @patch("infrastructure.config.Config.SecretManager")
    def test_loads_env_and_secrets(self, mock_secret_manager_class):
        # Arrange
        os.environ["ENV"] = "test"
        os.environ["SECRETS_NAME"] = "my-secret"
        os.environ["SECRETS_REGION"] = "eu-west-1"

        mock_secret_manager_instance = MagicMock()
        mock_secret_manager_instance.get_secrets.return_value = {
            "DATABASE_URL": "postgres://user:pass@host/db",
            "ENV": "secret",  # Override test value
        }
        mock_secret_manager_class.return_value = mock_secret_manager_instance

        config = Config()

        # Act
        env = config.get("ENV")
        db_url = config.get("DATABASE_URL")

        # Assert
        assert env == "secret"
        assert db_url == "postgres://user:pass@host/db"
        assert config.init is True

        mock_secret_manager_class.assert_called_once_with(
            secret_name="my-secret", secret_region="eu-west-1", secret_endpoint=None
        )

    @patch("infrastructure.config.Config.SecretManager")
    def test_uses_only_env_when_no_secrets(self, mock_secret_manager_class):
        # Arrange
        os.environ["ENV"] = "dev"
        os.environ.pop("SECRETS_NAME", None)
        os.environ.pop("SECRETS_REGION", None)

        config = Config()

        # Act
        env = config.get("ENV")

        # Assert
        assert env == "dev"
        assert config.init is True
        mock_secret_manager_class.assert_not_called()

    def test_returns_empty_string_for_missing_key(self):
        # Arrange
        os.environ.clear()
        os.environ["ENV"] = "testing"
        os.environ.pop("SECRETS_NAME", None)
        os.environ.pop("SECRETS_REGION", None)

        config = Config()

        # Act
        missing = config.get("NOT_DEFINED")

        # Assert
        assert missing == ""

    @patch("os.environ.items")
    def test_loads_secrets_only_once(self, os_environ_items):
        # Arrange
        os.environ.clear()
        os.environ["ENV"] = "testing"
        os.environ.pop("SECRETS_NAME", None)
        os.environ.pop("SECRETS_REGION", None)

        config = Config()
        config.get("ENV")
        config.get("ENV")

        os_environ_items.assert_called_once()

    @pytest.fixture(autouse=True)
    def reset_config_class_state(self):
        # Run before each test
        Config.config = {}
        Config.init = False
        yield
        # Run after each test
        Config.config = {}
        Config.init = False
