from datetime import datetime, timezone
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from packages.capability_engine.registry import registry
from packages.capability_engine.models import CapabilityDefinition

class CommandExecutionResult(BaseModel):
    """
    Structured outcome of a capability execution mapping to Section 24 requirements.
    """
    execution_id: str
    capability_id: str
    target_device_ids: List[str]
    source_interface: str
    status: str  # "success", "failed", "pending", "requires_confirmation"
    start_time: datetime
    end_time: Optional[datetime] = None
    outcome: Optional[str] = None
    result_payload: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    trace_id: Optional[str] = None
    selected_adapter: Optional[str] = None

class CommandRequest(BaseModel):
    """
    A structured request to invoke a specific capability on target devices.
    """
    capability_id: str
    target_device_ids: List[str]
    parameters: Dict[str, Any] = Field(default_factory=dict)
    source_interface: str = "api"
    actor_id: Optional[str] = None
    trace_id: Optional[str] = None
    force_confirmation: bool = False

def _now_utc() -> datetime:
    return datetime.now(timezone.utc)

class CommandExecutionEngine:
    """
    The core engine responsible for receiving capability requests,
    validating parameters against the definition, checking safety policies,
    and delegating to the appropriate device adapter (mocked here for now).
    """
    def __init__(self, capability_registry=registry):
        self.registry = capability_registry
        # In the future, this engine will depend on the DeviceRegistry and AdapterRegistry

    def execute_command(self, request: CommandRequest) -> CommandExecutionResult:
        """
        Executes a command synchronously.
        Records lifecycle start and handles validation.
        """
        execution_id = str(uuid.uuid4())
        start_time = _now_utc()

        result = CommandExecutionResult(
            execution_id=execution_id,
            capability_id=request.capability_id,
            target_device_ids=request.target_device_ids,
            source_interface=request.source_interface,
            status="pending",
            start_time=start_time,
            trace_id=request.trace_id
        )

        try:
            # 1. Resolve Capability
            capability = self.registry.get(request.capability_id)
            if not capability:
                raise ValueError(f"Unknown capability: {request.capability_id}")

            # 2. Validate Parameters
            self._validate_parameters(capability, request.parameters)

            # 3. Apply Safety & Confirmation Policy
            if self._requires_confirmation(capability, request):
                result.status = "requires_confirmation"
                result.end_time = _now_utc()
                result.outcome = "Blocked pending user confirmation due to safety policy."
                return result

            # 4. Resolve Targets & Select Adapter
            # TODO: Integrate with packages/device_registry and packages/device_adapters_base
            # For now, we mock success if targets are provided
            if not request.target_device_ids:
                raise ValueError("No target devices specified for execution.")

            result.selected_adapter = "mock_adapter"

            # 5. Invoke Adapter (Mocked)
            # This is where we would normally call adapter.execute(capability, device, params)
            result.outcome = f"Executed {capability.name} successfully on {len(request.target_device_ids)} device(s)."
            result.result_payload = {"state_mutated": True}
            result.status = "success"

        except Exception as e:
            result.status = "failed"
            result.errors.append(str(e))
            result.outcome = "Execution failed due to an error."
        finally:
            result.end_time = _now_utc()

        # 6. Record Execution Lifecycle
        # TODO: Persist `result` and `request` to the DB using the `CommandExecution` model

        return result

    def _validate_parameters(self, capability: CapabilityDefinition, parameters: Dict[str, Any]) -> None:
        """
        Validates the requested parameters against the capability's JSON schema definition.
        """
        schema = capability.execution_contract.parameters_schema
        required_keys = schema.get("required", [])
        for req_key in required_keys:
            if req_key not in parameters:
                raise ValueError(f"Missing required parameter: '{req_key}'")

        # Simple type checking mock (in production, use jsonschema package or pydantic dynamically)
        props = schema.get("properties", {})
        for key, val in parameters.items():
            if key not in props:
                continue # Or raise error if strict
            expected_type = props[key].get("type")
            if expected_type == "integer" and not isinstance(val, int):
                raise ValueError(f"Parameter '{key}' must be of type integer.")
            elif expected_type == "string" and not isinstance(val, str):
                raise ValueError(f"Parameter '{key}' must be of type string.")

    def _requires_confirmation(self, capability: CapabilityDefinition, request: CommandRequest) -> bool:
        if request.force_confirmation:
            return True
        if capability.default_confirmation_policy == "always":
            return True
        if capability.safety_level == "dangerous":
            return True
        return False
