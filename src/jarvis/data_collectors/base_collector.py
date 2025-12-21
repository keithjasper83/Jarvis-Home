"""
Base Data Collector

Abstract base class for all data collectors.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
import logging

from ..models.device_data import DeviceData


class BaseCollector(ABC):
    """
    Abstract base class for device data collectors.
    
    All device-specific collectors should inherit from this class
    and implement the required abstract methods.
    """
    
    def __init__(self, name: str, config: dict):
        """
        Initialize the collector.
        
        Args:
            name: Name of the collector
            config: Configuration dictionary for the collector
        """
        self.name = name
        self.config = config
        self.logger = logging.getLogger(f"jarvis.collector.{name}")
        self._connected = False
        self._last_collection_time: Optional[datetime] = None
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the device or service.
        
        Returns:
            True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """
        Close connection to the device or service.
        
        Returns:
            True if disconnection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def collect_data(self) -> List[DeviceData]:
        """
        Collect data from the device or service.
        
        Returns:
            List of DeviceData objects containing collected data
        """
        pass
    
    def is_connected(self) -> bool:
        """Check if the collector is connected."""
        return self._connected
    
    def get_last_collection_time(self) -> Optional[datetime]:
        """Get the timestamp of the last data collection."""
        return self._last_collection_time
    
    def validate_config(self) -> bool:
        """
        Validate the collector configuration.
        
        Subclasses should override this method to add specific validation
        for their required configuration parameters.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not self.config:
            self.logger.error("Configuration is empty")
            return False
        
        return True
