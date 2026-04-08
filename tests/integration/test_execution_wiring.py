import unittest
from packages.capability_engine.execution import CommandExecutionEngine, CommandRequest
from packages.capability_engine.registry import CapabilityRegistry
from packages.capability_engine.models import CapabilityDefinition, ExecutionContract
from packages.device_adapters_base.registry import AdapterRegistry
from packages.device_adapters_base.adapter import BaseAdapter, AdapterExecutionResult

# Create a mock adapter to inject
class MockWiredAdapter(BaseAdapter):
    @property
    def adapter_id(self): return "wired.mock"
    @property
    def supported_device_types(self): return []
    @property
    def supported_capabilities(self): return ["system.test"]
    def test_connection(self, host, creds=None): pass
    def probe(self, host, creds=None): pass
    def get_capabilities(self, host): pass
    def get_status(self, host, cap_id, creds=None): pass
    def validate_config(self, config): pass
    def interrogate(self, host, creds=None): pass

    def execute_command(self, host, capability_id, parameters, creds=None):
        if parameters.get("fail_please"):
            return AdapterExecutionResult(success=False, error_message="Simulated Failure")
        return AdapterExecutionResult(success=True, payload={"host_targeted": host, "cap": capability_id})

# Create a mock device registry to inject
class MockDeviceRegistry:
    class MockDevice:
        def __init__(self, host, adapter_id):
            self.host = host
            self.adapter_id = adapter_id

    def get_device(self, device_id):
        if device_id == "dev_123":
            return self.MockDevice(host="192.168.1.5", adapter_id="wired.mock")
        return None

class TestExecutionWiring(unittest.TestCase):
    def setUp(self):
        # 1. Setup Capability
        self.cap_registry = CapabilityRegistry()
        self.cap_registry.register(CapabilityDefinition(
            capability_id="system.test",
            name="Test System",
            description="Tests the wiring.",
            category="testing",
            execution_contract=ExecutionContract(
                parameters_schema={
                    "type": "object",
                    "properties": {
                        "fail_please": {"type": "boolean"}
                    }
                }
            )
        ))

        # 2. Setup Device Registry
        self.device_registry = MockDeviceRegistry()

        # 3. Setup Adapter Registry
        self.adapter_registry = AdapterRegistry()
        self.adapter_registry.register(MockWiredAdapter())

        # 4. Engine
        self.engine = CommandExecutionEngine(
            capability_registry=self.cap_registry,
            device_registry=self.device_registry,
            adapter_registry=self.adapter_registry
        )

    def test_end_to_end_wiring_success(self):
        request = CommandRequest(
            capability_id="system.test",
            target_device_ids=["dev_123"],
            parameters={"fail_please": False}
        )
        result = self.engine.execute_command(request)

        self.assertEqual(result.status, "success")
        self.assertEqual(result.selected_adapter, "wired.mock")
        self.assertEqual(result.result_payload["host_targeted"], "192.168.1.5")

    def test_end_to_end_wiring_failure(self):
        request = CommandRequest(
            capability_id="system.test",
            target_device_ids=["dev_123"],
            parameters={"fail_please": True}
        )
        result = self.engine.execute_command(request)

        self.assertEqual(result.status, "failed")
        self.assertEqual(result.selected_adapter, "wired.mock")
        self.assertIn("Simulated Failure", result.errors)

    def test_wiring_unknown_device(self):
        request = CommandRequest(
            capability_id="system.test",
            target_device_ids=["unknown_dev"],
            parameters={}
        )
        result = self.engine.execute_command(request)

        self.assertEqual(result.status, "failed")
        self.assertTrue(any("Device not found" in err for err in result.errors))

if __name__ == "__main__":
    unittest.main()
