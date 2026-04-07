from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from infra.db.models import Device

class DeviceRegistry:
    """
    Handles CRUD operations and inventory logic for devices defined in Section 19.
    Provides persistence for device model mapping, registration, and capabilities.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_device(self, device_data: Dict[str, Any]) -> Device:
        """Registers a new device into the system."""
        device = Device(**device_data)
        self.session.add(device)
        self.session.commit()
        self.session.refresh(device)
        return device

    def get_device(self, device_id: str) -> Optional[Device]:
        """Retrieves a specific device by its unique ID."""
        return self.session.query(Device).filter(Device.id == device_id).first()

    def list_devices(self, filters: Optional[Dict[str, Any]] = None) -> List[Device]:
        """
        Lists inventory devices. Supports basic filtering by kwargs
        (e.g., {"room": "kitchen", "device_type": "light"}).
        """
        query = self.session.query(Device)
        if filters:
            for key, value in filters.items():
                if hasattr(Device, key):
                    query = query.filter(getattr(Device, key) == value)
        return query.all()

    def update_device(self, device_id: str, updates: Dict[str, Any]) -> Optional[Device]:
        """Updates specific fields of an existing device."""
        device = self.get_device(device_id)
        if not device:
            return None

        for key, value in updates.items():
            if hasattr(device, key):
                setattr(device, key, value)

        self.session.commit()
        self.session.refresh(device)
        return device

    def delete_device(self, device_id: str) -> bool:
        """Removes a device from the registry."""
        device = self.get_device(device_id)
        if not device:
            return False

        self.session.delete(device)
        self.session.commit()
        return True
