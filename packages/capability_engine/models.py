from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class SafetyLevel(str, Enum):
    SAFE = "safe"              # Read-only or non-mutating (e.g., status query)
    MODERATE = "moderate"      # Reversible or low-impact (e.g., lights on/off)
    ELEVATED = "elevated"      # Disruptive or resource-heavy (e.g., thermostat temp)
    DANGEROUS = "dangerous"    # Physical risk or high-security (e.g., unlock door, oven on)

class ConfirmationPolicy(str, Enum):
    NONE = "none"              # Execute immediately
    OPTIONAL = "optional"      # Ask for confirmation if ambiguity exists
    ALWAYS = "always"          # Mandatory user confirmation before execution

class ExecutionContract(BaseModel):
    """
    Defines the expected input parameters and output results for a capability execution.
    `parameters_schema` is a JSON Schema definition of required arguments.
    """
    parameters_schema: Dict[str, Any] = Field(default_factory=dict)
    returns_status: bool = False
    is_async: bool = False

class CapabilityDefinition(BaseModel):
    """
    The shared capability model defining a system action available across voice and web.
    """
    capability_id: str
    name: str
    description: str
    category: str

    target_device_types: List[str] = Field(default_factory=list)

    # Required/Optional contextual fields required beyond standard parameters
    required_context: List[str] = Field(default_factory=list)
    optional_context: List[str] = Field(default_factory=list)

    safety_level: SafetyLevel = SafetyLevel.MODERATE
    default_confirmation_policy: ConfirmationPolicy = ConfirmationPolicy.NONE

    execution_contract: ExecutionContract = Field(default_factory=ExecutionContract)

    status_query_support: bool = False

    # UI and Voice specific metadata
    voice_examples: List[str] = Field(default_factory=list)
    ui_rendering_hints: Dict[str, Any] = Field(default_factory=dict)
    adapter_compatibility: List[str] = Field(default_factory=list)
