import unittest
from unittest.mock import patch, MagicMock
from packages.device_adapters_http.adapter import HttpLocalAdapter

class TestHttpLocalAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = HttpLocalAdapter()

    def test_adapter_properties(self):
        self.assertEqual(self.adapter.adapter_id, "http.local")
        self.assertIn("light", self.adapter.supported_device_types)
        self.assertIn("light.on", self.adapter.supported_capabilities)

    def test_build_url(self):
        self.assertEqual(self.adapter._build_url("192.168.1.10", "/test"), "http://192.168.1.10/test")
        self.assertEqual(self.adapter._build_url("https://tapo.local", "/api"), "https://tapo.local/api")

    @patch('urllib.request.urlopen')
    def test_execute_command_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"state": "on"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = self.adapter.execute_command(
            host="192.168.1.10",
            capability_id="light.on",
            parameters={"brightness": 100}
        )

        self.assertTrue(result.success)
        self.assertEqual(result.payload, {"state": "on"})
        # Verify the requested URL translation
        args, kwargs = mock_urlopen.call_args
        req = args[0]
        self.assertEqual(req.full_url, "http://192.168.1.10/api/commands/light/on")
        self.assertEqual(req.data, b'{"brightness": 100}')

    @patch('urllib.request.urlopen')
    def test_execute_command_failure(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Connection Refused")

        result = self.adapter.execute_command(
            host="192.168.1.10",
            capability_id="light.on",
            parameters={}
        )

        self.assertFalse(result.success)
        self.assertEqual(result.error_message, "Connection Refused")

if __name__ == "__main__":
    unittest.main()
