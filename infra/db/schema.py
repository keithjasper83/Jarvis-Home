from datetime import datetime

# Stub schema file — NOT intended to be imported as runtime ORM models yet.
# Entities: users, deployments, ui_overrides, devices, device_aliases, etc.
# Full implementation will use SQLAlchemy / SQLModel.

class DevicePlaceholder:
    id: str
    friendly_name: str
    device_type: str
    protocol: str
    host: str
    enabled: bool
    created_at: datetime
    updated_at: datetime

class CapabilityPlaceholder:
    id: str
    capability_key: str
    display_name: str
    category: str

# To be implemented completely with SQLAlchemy / SQLModel
