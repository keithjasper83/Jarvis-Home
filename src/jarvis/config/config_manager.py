"""
Configuration Manager

Handles loading and validation of configuration files.
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """
    Manages configuration loading and access for Jarvis.
    
    Supports YAML configuration files and environment variables.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to configuration file. If None, uses default location.
        """
        self.logger = logging.getLogger("jarvis.config")
        self.config_path = config_path or self._get_default_config_path()
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get the default configuration file path."""
        # Check for config in current directory
        if os.path.exists('config/config.yaml'):
            return 'config/config.yaml'
        
        # Check for config in user's home directory
        home_config = Path.home() / '.jarvis' / 'config.yaml'
        if home_config.exists():
            return str(home_config)
        
        # Use default config directory
        return 'config/config.yaml'
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self._config = yaml.safe_load(f) or {}
                self.logger.info(f"Loaded configuration from {self.config_path}")
            else:
                self.logger.warning(f"Configuration file not found: {self.config_path}")
                self._config = self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'collectors': {
                'shelly': {
                    'enabled': False,
                    'devices': []
                },
                'tapo': {
                    'enabled': False,
                    'devices': []
                },
                'alexa': {
                    'enabled': False,
                    'devices': []
                },
                'windows': {
                    'enabled': False,
                    'host': 'localhost'
                },
                'mac': {
                    'enabled': False,
                    'host': 'localhost'
                }
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'data_collection': {
                'interval': 60,  # seconds
                'storage_path': 'data/collected'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'collectors.shelly.enabled')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_collector_config(self, collector_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific collector.
        
        Args:
            collector_name: Name of the collector
            
        Returns:
            Collector configuration dictionary
        """
        return self.get(f'collectors.{collector_name}', {})
    
    def is_collector_enabled(self, collector_name: str) -> bool:
        """
        Check if a collector is enabled.
        
        Args:
            collector_name: Name of the collector
            
        Returns:
            True if collector is enabled
        """
        return self.get(f'collectors.{collector_name}.enabled', False)
    
    def get_all_enabled_collectors(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all enabled collectors with their configurations.
        
        Returns:
            Dictionary mapping collector names to their configurations
        """
        enabled_collectors = {}
        collectors = self.get('collectors', {})
        
        for name, config in collectors.items():
            if config.get('enabled', False):
                enabled_collectors[name] = config
        
        return enabled_collectors
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()
        self.logger.info("Configuration reloaded")
