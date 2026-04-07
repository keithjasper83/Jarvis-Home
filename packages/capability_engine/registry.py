from typing import Dict, List, Optional
from packages.capability_engine.models import CapabilityDefinition

class CapabilityRegistry:
    """
    An in-memory registry resolving capability models by their ID.
    Future iterations may hydrate this from the database or merge with local JSON/YAML stores.
    """
    def __init__(self):
        self._capabilities: Dict[str, CapabilityDefinition] = {}

    def register(self, definition: CapabilityDefinition) -> None:
        """Registers a new capability definition."""
        if definition.capability_id in self._capabilities:
            raise ValueError(f"Capability with ID '{definition.capability_id}' is already registered.")
        self._capabilities[definition.capability_id] = definition

    def get(self, capability_id: str) -> Optional[CapabilityDefinition]:
        """Retrieves a capability by its exact ID."""
        return self._capabilities.get(capability_id)

    def list_all(self) -> List[CapabilityDefinition]:
        """Lists all registered capabilities."""
        return list(self._capabilities.values())

    def search_by_category(self, category: str) -> List[CapabilityDefinition]:
        """Returns all capabilities belonging to a specific category."""
        return [cap for cap in self._capabilities.values() if cap.category == category]

    def clear(self) -> None:
        """Clears the registry (useful for testing)."""
        self._capabilities.clear()

# Global registry instance
registry = CapabilityRegistry()
