from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class AdapterHealth(BaseModel):
    is_healthy: bool
    status_message: str
    latency_ms: Optional[int] = None

class AdapterExecutionResult(BaseModel):
    success: bool
    payload: Dict[str, Any] = {}
    error_message: Optional[str] = None

class BaseAdapter(ABC):
    """
    Abstract Base Class for all Device Adapters (e.g. HTTP, SSH, MQTT).
    Defines the contract for Section 20 requirements.
    """

    @property
    @abstractmethod
    def adapter_id(self) -> str:
        """A unique identifier for the adapter class (e.g., 'http.local', 'ssh.tapo')."""
        pass

    @property
    @abstractmethod
    def supported_device_types(self) -> List[str]:
        """List of device type strings this adapter handles."""
        pass

    @property
    @abstractmethod
    def supported_capabilities(self) -> List[str]:
        """List of capability_ids this adapter can execute."""
        pass

    @abstractmethod
    def test_connection(self, host: str, credentials_ref: Optional[str] = None) -> AdapterHealth:
        """Verifies if the adapter can establish communication with the target device."""
        pass

    @abstractmethod
    def probe(self, host: str, credentials_ref: Optional[str] = None) -> Dict[str, Any]:
        """Attempts to discover detailed device identity/state (read-only)."""
        pass

    @abstractmethod
    def get_capabilities(self, host: str) -> List[str]:
        """Dynamically retrieves capabilities exposed by a specific target."""
        pass

    @abstractmethod
    def get_status(self, host: str, capability_id: str, credentials_ref: Optional[str] = None) -> Dict[str, Any]:
        """Queries current status for a specific capability on the target."""
        pass

    @abstractmethod
    def execute_command(
        self,
        host: str,
        capability_id: str,
        parameters: Dict[str, Any],
        credentials_ref: Optional[str] = None
    ) -> AdapterExecutionResult:
        """
        Executes an automation command securely over the adapter's protocol.
        """
        pass

    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validates configuration schema specific to the adapter."""
        pass

    @abstractmethod
    def interrogate(self, host: str, credentials_ref: Optional[str] = None) -> Dict[str, Any]:
        """Runs deeper investigative read-only workflows mapping to Section 22 Interrogation."""
        pass
