"""
Device Data Model

Represents data collected from a smart home device.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class DeviceData:
    """
    Data model for device information and readings.
    
    Attributes:
        device_id: Unique identifier for the device
        device_type: Type of device (e.g., 'shelly', 'tapo', 'alexa')
        device_name: Human-readable name of the device
        timestamp: When the data was collected
        data: Dictionary containing device-specific data
        status: Current status of the device (e.g., 'online', 'offline')
        metadata: Additional metadata about the collection
    """
    device_id: str
    device_type: str
    device_name: str
    timestamp: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)
    status: str = "unknown"
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the device data to a dictionary."""
        return {
            'device_id': self.device_id,
            'device_type': self.device_type,
            'device_name': self.device_name,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data,
            'status': self.status,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DeviceData':
        """Create a DeviceData instance from a dictionary."""
        # Create a copy to avoid mutating the input dictionary
        data_copy = data.copy()
        timestamp_str = data_copy.get('timestamp')
        if timestamp_str:
            data_copy['timestamp'] = datetime.fromisoformat(timestamp_str)
        return cls(**data_copy)
