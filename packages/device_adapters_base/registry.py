from typing import Dict, Optional, List
from .adapter import BaseAdapter

class AdapterRegistry:
    """
    Manages active, instantiated device adapters.
    Provides lookup capabilities for the Command Execution Engine to route commands
    based on the target device's configured protocol or adapter binding.
    """
    def __init__(self):
        self._adapters: Dict[str, BaseAdapter] = {}

    def register(self, adapter: BaseAdapter) -> None:
        """Registers an instantiated adapter instance."""
        if adapter.adapter_id in self._adapters:
            raise ValueError(f"Adapter with ID '{adapter.adapter_id}' is already registered.")
        self._adapters[adapter.adapter_id] = adapter

    def get(self, adapter_id: str) -> Optional[BaseAdapter]:
        """Retrieves an adapter by its ID."""
        return self._adapters.get(adapter_id)

    def list_all(self) -> List[BaseAdapter]:
        """Returns all registered adapters."""
        return list(self._adapters.values())

    def clear(self) -> None:
        self._adapters.clear()

# Global adapter registry instance
registry = AdapterRegistry()
