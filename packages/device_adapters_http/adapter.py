from typing import Dict, Any, List, Optional
from packages.device_adapters_base.adapter import BaseAdapter, AdapterHealth, AdapterExecutionResult
import urllib.request
import json

class HttpLocalAdapter(BaseAdapter):
    """
    HTTP-based local control adapter.
    Executes commands securely using HTTP/HTTPS against local targets.
    """
    @property
    def adapter_id(self) -> str:
        return "http.local"

    @property
    def supported_device_types(self) -> List[str]:
        return ["light", "switch", "sensor", "media", "camera"]

    @property
    def supported_capabilities(self) -> List[str]:
        return ["light.on", "light.off", "switch.on", "switch.off"]

    def _build_url(self, host: str, path: str = "/") -> str:
        if not host.startswith("http"):
            return f"http://{host}{path}"
        return f"{host}{path}"

    def test_connection(self, host: str, credentials_ref: Optional[str] = None) -> AdapterHealth:
        url = self._build_url(host, "/health")
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    return AdapterHealth(is_healthy=True, status_message="OK")
        except Exception as e:
            return AdapterHealth(is_healthy=False, status_message=str(e))
        return AdapterHealth(is_healthy=False, status_message="Non-200 Response")

    def probe(self, host: str, credentials_ref: Optional[str] = None) -> Dict[str, Any]:
        """Probes the device identity over HTTP (e.g. fetching /info)."""
        url = self._build_url(host, "/info")
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
        except Exception:
            pass
        return {}

    def get_capabilities(self, host: str) -> List[str]:
        return self.supported_capabilities

    def get_status(self, host: str, capability_id: str, credentials_ref: Optional[str] = None) -> Dict[str, Any]:
        url = self._build_url(host, f"/status/{capability_id.replace('.', '/')}")
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception:
            return {"status": "unknown"}

    def execute_command(
        self,
        host: str,
        capability_id: str,
        parameters: Dict[str, Any],
        credentials_ref: Optional[str] = None
    ) -> AdapterExecutionResult:
        """
        Executes a command by dispatching an HTTP POST to the target.
        Converts the capability ID to a predictable path.
        """
        path = f"/api/commands/{capability_id.replace('.', '/')}"
        url = self._build_url(host, path)
        data = json.dumps(parameters).encode('utf-8')

        headers = {'Content-Type': 'application/json'}
        # In a real system, credentials_ref would fetch API tokens from a secure vault
        # and attach them to headers or auth.

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status in (200, 201, 202, 204):
                    payload_str = response.read().decode('utf-8')
                    payload = json.loads(payload_str) if payload_str else {}
                    return AdapterExecutionResult(success=True, payload=payload)
                else:
                    return AdapterExecutionResult(success=False, error_message=f"HTTP {response.status}")
        except Exception as e:
            return AdapterExecutionResult(success=False, error_message=str(e))

    def validate_config(self, config: Dict[str, Any]) -> bool:
        return "host" in config

    def interrogate(self, host: str, credentials_ref: Optional[str] = None) -> Dict[str, Any]:
        """Deep inspection over HTTP."""
        return {
            "info": self.probe(host, credentials_ref),
            "health": self.test_connection(host, credentials_ref).dict()
        }
