import unittest
from packages.capability_engine.models import CapabilityDefinition, ExecutionContract, SafetyLevel, ConfirmationPolicy
from packages.capability_engine.registry import CapabilityRegistry
from packages.capability_engine.execution import CommandExecutionEngine, CommandRequest

class TestCapabilityEngine(unittest.TestCase):
    def setUp(self):
        self.registry = CapabilityRegistry()
        self.engine = CommandExecutionEngine(capability_registry=self.registry)

        self.light_cap = CapabilityDefinition(
            capability_id="light.set_brightness",
            name="Set Brightness",
            description="Adjusts light brightness.",
            category="lighting",
            safety_level=SafetyLevel.MODERATE,
            default_confirmation_policy=ConfirmationPolicy.NONE,
            execution_contract=ExecutionContract(
                parameters_schema={
                    "type": "object",
                    "properties": {
                        "level": {"type": "integer"}
                    },
                    "required": ["level"]
                }
            )
        )
        self.dangerous_cap = CapabilityDefinition(
            capability_id="door.unlock",
            name="Unlock Door",
            description="Unlocks the front door.",
            category="security",
            safety_level=SafetyLevel.DANGEROUS,
            default_confirmation_policy=ConfirmationPolicy.ALWAYS,
        )
        self.registry.register(self.light_cap)
        self.registry.register(self.dangerous_cap)

    def test_registry_storage(self):
        self.assertEqual(len(self.registry.list_all()), 2)
        self.assertEqual(self.registry.get("light.set_brightness").name, "Set Brightness")

    def test_command_execution_success(self):
        request = CommandRequest(
            capability_id="light.set_brightness",
            target_device_ids=["dev_123"],
            parameters={"level": 50}
        )
        result = self.engine.execute_command(request)

        self.assertEqual(result.status, "success")
        self.assertEqual(result.capability_id, "light.set_brightness")
        self.assertIsNotNone(result.end_time)
        self.assertTrue(result.result_payload.get("state_mutated"))

    def test_command_execution_validation_failure(self):
        # Missing required parameter "level"
        request = CommandRequest(
            capability_id="light.set_brightness",
            target_device_ids=["dev_123"],
            parameters={}
        )
        result = self.engine.execute_command(request)

        self.assertEqual(result.status, "failed")
        self.assertTrue(any("Missing required parameter" in err for err in result.errors))

    def test_command_execution_type_failure(self):
        # Wrong type for parameter "level" (string instead of int)
        request = CommandRequest(
            capability_id="light.set_brightness",
            target_device_ids=["dev_123"],
            parameters={"level": "high"}
        )
        result = self.engine.execute_command(request)

        self.assertEqual(result.status, "failed")
        self.assertTrue(any("must be of type integer" in err for err in result.errors))

    def test_command_execution_safety_confirmation(self):
        # Requesting a dangerous action should block and require confirmation
        request = CommandRequest(
            capability_id="door.unlock",
            target_device_ids=["dev_999"]
        )
        result = self.engine.execute_command(request)

        self.assertEqual(result.status, "requires_confirmation")
        self.assertIn("Blocked", result.outcome)

if __name__ == "__main__":
    unittest.main()
