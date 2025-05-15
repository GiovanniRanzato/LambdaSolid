from abc import ABC, abstractmethod


class SecretManagerI(ABC):
    @abstractmethod
    def get_secrets(self) -> dict:
        """Get config from config manager"""