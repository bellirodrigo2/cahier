""" Interfaces for module loading and injecting"""
from typing import Protocol, Any

class Injectable(Protocol):
    """Represents an Injectable Object Interface"""

    def inject(self, tgt: Any) -> None:
        """Inject a Generic target object to the injectable."""
        pass


class ModuleInterface:
    """Represents a plugin interface. A plugin has a single register function."""

    @staticmethod
    def register(injectable: Injectable) -> None:
        """Register the Obj Attribute in Cahier."""
