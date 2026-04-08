from typing import Dict, Any, List, Optional
import paramiko
from packages.device_adapters_base.adapter import BaseAdapter, AdapterHealth, AdapterExecutionResult

class SshLocalAdapter(BaseAdapter):
    """
    SSH-based adapter for direct shell interrogation and mutating command execution.
    Targeted towards devices or servers that allow secure shell access, such as Raspberry Pis
    or linux-based gateways.
    """

    @property
    def adapter_id(self) -> str:
        return "ssh.local"

    @property
    def supported_device_types(self) -> List[str]:
        # Typically generalized compute systems, custom DIY boards, or router/switches
        return ["server", "compute", "gateway", "tapo", "custom"]

    @property
    def supported_capabilities(self) -> List[str]:
        # Often mapped dynamically via bash scripts, but these are general stubs
        return ["system.reboot", "service.restart", "device.status_query"]

    def _get_ssh_client(self, host: str, credentials_ref: Optional[str] = None) -> paramiko.SSHClient:
        """
        Builds and connects a paramiko SSH client.
        In the future, credentials_ref fetches from a secure credential store.
        """
        import os
        # Fallback credentials driven by environment configuration, avoiding hardcoded secrets in source control.
        username = os.environ.get("SSH_DEFAULT_USER")
        password = os.environ.get("SSH_DEFAULT_PASS")

        if not username or not password:
            raise ValueError("SSH credentials not configured. Please provide them securely.")

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # We don't actually connect during unit tests without a mock, so timeout is low
        client.connect(hostname=host, username=username, password=password, timeout=3.0)
        return client

    def test_connection(self, host: str, credentials_ref: Optional[str] = None) -> AdapterHealth:
        try:
            with self._get_ssh_client(host, credentials_ref) as client:
                stdin, stdout, stderr = client.exec_command("echo 'healthy'")
                output = stdout.read().decode('utf-8').strip()
                if "healthy" in output:
                    return AdapterHealth(is_healthy=True, status_message="OK")
        except paramiko.AuthenticationException:
            return AdapterHealth(is_healthy=False, status_message="Authentication Failed")
        except Exception as e:
            return AdapterHealth(is_healthy=False, status_message=str(e))
        return AdapterHealth(is_healthy=False, status_message="Unknown Error")

    def probe(self, host: str, credentials_ref: Optional[str] = None) -> Dict[str, Any]:
        """Investigates device identity by running `uname` or reading release files."""
        try:
            with self._get_ssh_client(host, credentials_ref) as client:
                _, stdout, _ = client.exec_command("uname -a")
                uname_info = stdout.read().decode('utf-8').strip()
                return {"os": uname_info, "protocol": "ssh"}
        except Exception:
            pass
        return {}

    def get_capabilities(self, host: str) -> List[str]:
        # Dynamic discovery could parse specific bin scripts over SSH
        return self.supported_capabilities

    def get_status(self, host: str, capability_id: str, credentials_ref: Optional[str] = None) -> Dict[str, Any]:
        """Runs a status check script on the target depending on the capability."""
        # e.g., systemctl status <service>
        return {"status": "unknown"}

    def execute_command(
        self,
        host: str,
        capability_id: str,
        parameters: Dict[str, Any],
        credentials_ref: Optional[str] = None
    ) -> AdapterExecutionResult:
        """
        Executes a shell command corresponding to a capability.
        """
        # Map capability_id to a safe shell command
        # This is a stubbed mapping logic
        command = f"echo 'Mock execution of {capability_id}'"
        if capability_id == "system.reboot":
            command = "sudo reboot"

        try:
            with self._get_ssh_client(host, credentials_ref) as client:
                stdin, stdout, stderr = client.exec_command(command)
                exit_status = stdout.channel.recv_exit_status()

                if exit_status == 0:
                    payload_str = stdout.read().decode('utf-8').strip()
                    return AdapterExecutionResult(success=True, payload={"stdout": payload_str})
                else:
                    err_str = stderr.read().decode('utf-8').strip()
                    return AdapterExecutionResult(success=False, error_message=f"Exit {exit_status}: {err_str}")
        except Exception as e:
            return AdapterExecutionResult(success=False, error_message=str(e))

    def validate_config(self, config: Dict[str, Any]) -> bool:
        return "host" in config

    def interrogate(self, host: str, credentials_ref: Optional[str] = None) -> Dict[str, Any]:
        """Deep investigation over SSH."""
        try:
            with self._get_ssh_client(host, credentials_ref) as client:
                _, out_banners, _ = client.exec_command("cat /etc/os-release || echo 'unknown'")
                os_release = out_banners.read().decode('utf-8').strip()

                _, out_ports, _ = client.exec_command("netstat -tuln || ss -tuln || echo 'unknown'")
                ports = out_ports.read().decode('utf-8').strip()

                return {
                    "os_release": os_release,
                    "listening_ports": ports,
                    "local_control_confidence": 0.9
                }
        except Exception as e:
            return {"error": str(e), "local_control_confidence": 0.0}
