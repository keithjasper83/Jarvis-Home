import unittest
from unittest.mock import patch, MagicMock
import paramiko
from packages.device_adapters_ssh.adapter import SshLocalAdapter

class TestSshLocalAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = SshLocalAdapter()

    def test_adapter_properties(self):
        self.assertEqual(self.adapter.adapter_id, "ssh.local")
        self.assertIn("server", self.adapter.supported_device_types)
        self.assertIn("system.reboot", self.adapter.supported_capabilities)

    @patch('os.environ.get')
    @patch('packages.device_adapters_ssh.adapter.paramiko.SSHClient')
    def test_execute_command_success(self, MockSSHClient, mock_env_get):
        # Provide fallback credentials
        mock_env_get.side_effect = lambda k: "admin" if k == "SSH_DEFAULT_USER" else "password"
        # Mock the SSH client and its connection/execution lifecycle
        mock_client_instance = MagicMock()
        MockSSHClient.return_value = mock_client_instance

        # Mock the context manager (__enter__ / __exit__)
        mock_client_instance.__enter__.return_value = mock_client_instance

        # Mock the exec_command returns
        mock_stdout = MagicMock()
        mock_stderr = MagicMock()
        mock_stdout.channel.recv_exit_status.return_value = 0
        mock_stdout.read.return_value = b'Restarting system...\n'

        mock_client_instance.exec_command.return_value = (None, mock_stdout, mock_stderr)

        result = self.adapter.execute_command(
            host="192.168.1.100",
            capability_id="system.reboot",
            parameters={}
        )

        self.assertTrue(result.success)
        self.assertEqual(result.payload, {"stdout": "Restarting system..."})

        # Ensure the correct capability was mapped to the correct shell command
        mock_client_instance.exec_command.assert_called_with("sudo reboot")
        mock_client_instance.connect.assert_called_once_with(
            hostname="192.168.1.100", username="admin", password="password", timeout=3.0
        )

    @patch('os.environ.get')
    @patch('packages.device_adapters_ssh.adapter.paramiko.SSHClient')
    def test_execute_command_auth_failure(self, MockSSHClient, mock_env_get):
        # Provide fallback credentials
        mock_env_get.side_effect = lambda k: "admin" if k == "SSH_DEFAULT_USER" else "password"
        mock_client_instance = MagicMock()
        MockSSHClient.return_value = mock_client_instance

        # Simulate authentication failure
        mock_client_instance.connect.side_effect = paramiko.AuthenticationException("Auth failed")

        result = self.adapter.execute_command(
            host="192.168.1.100",
            capability_id="system.reboot",
            parameters={}
        )

        self.assertFalse(result.success)
        self.assertEqual(result.error_message, "Auth failed")

if __name__ == "__main__":
    unittest.main()
