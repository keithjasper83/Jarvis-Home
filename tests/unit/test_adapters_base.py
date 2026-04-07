import unittest
from packages.device_adapters_base.adapter import BaseAdapter

class MockValidAdapter(BaseAdapter):
    @property
    def adapter_id(self): return "mock"

    @property
    def supported_device_types(self): return ["mock_type"]

    @property
    def supported_capabilities(self): return ["mock.on"]

    def test_connection(self, host, creds=None): pass
    def probe(self, host, creds=None): pass
    def get_capabilities(self, host): pass
    def get_status(self, host, cap_id, creds=None): pass
    def execute_command(self, host, cap_id, params, creds=None): pass
    def validate_config(self, config): pass
    def interrogate(self, host, creds=None): pass


class MockInvalidAdapter(BaseAdapter):
    pass


class TestAdapterBase(unittest.TestCase):
    def test_adapter_abc_instantiation(self):
        # A valid implementation should instantiate properly
        valid = MockValidAdapter()
        self.assertEqual(valid.adapter_id, "mock")

        # Missing abstract methods should raise TypeError
        with self.assertRaises(TypeError):
            MockInvalidAdapter()

if __name__ == "__main__":
    unittest.main()
