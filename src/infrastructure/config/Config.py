import os

from dotenv import load_dotenv

from infrastructure.config.SecretManager import SecretManager
from infrastructure.interfaces.ConfigI import ConfigI


class Config(ConfigI):
    config = {}
    init = False

    def load(self):
        load_dotenv()
        items = os.environ.items()
        for item in items:
            self.config[item[0]] = item[1]
        if not self.init and self.config.get("SECRETS_NAME") and self.config.get("SECRETS_REGION"):
            secret_manager = SecretManager(
                secret_name=self.config["SECRETS_NAME"],
                secret_region=self.config["SECRETS_REGION"],
                secret_endpoint=self.config.get("SECRETS_ENDPOINT", None),
            )
            secret = secret_manager.get_secrets()
            self.config.update(secret)
        self.init = True

    def get(self, config_name: str) -> str:
        if not self.config and not self.init:
            self.load()
        return self.config.get(config_name, "")
