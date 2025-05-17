from abc import ABC, abstractmethod


class ConfigI(ABC):
    @abstractmethod
    def load(self):
        """Get config from config manager"""

    @abstractmethod
    def get(self, config_name: str) -> str:
        """Get config from config manager"""
