"""
Jarvis Home Automation - Main Application

Main entry point for the Jarvis home automation system.
"""

import logging
import signal
import sys
import time
from typing import Dict, List
from datetime import datetime

# Add src directory to path for imports
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jarvis.config.config_manager import ConfigManager
from jarvis.data_collectors.base_collector import BaseCollector
from jarvis.data_collectors.shelly_collector import ShellyCollector
from jarvis.data_collectors.tapo_collector import TapoCollector
from jarvis.data_collectors.alexa_collector import AlexaCollector
from jarvis.data_collectors.windows_collector import WindowsCollector
from jarvis.data_collectors.mac_collector import MacCollector
from jarvis.models.device_data import DeviceData


class JarvisApp:
    """
    Main Jarvis application class.
    
    Orchestrates data collection from all configured collectors.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the Jarvis application.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = ConfigManager(config_path)
        self.collectors: Dict[str, BaseCollector] = {}
        self.running = False
        self._setup_logging()
        self.logger = logging.getLogger("jarvis.main")
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_level = self.config.get('logging.level', 'INFO')
        log_format = self.config.get('logging.format', 
                                     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format
        )
    
    def _signal_handler(self, signum, frame) -> None:
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
    
    def _initialize_collectors(self) -> None:
        """Initialize all enabled collectors."""
        self.logger.info("Initializing collectors...")
        
        enabled_collectors = self.config.get_all_enabled_collectors()
        
        collector_classes = {
            'shelly': ShellyCollector,
            'tapo': TapoCollector,
            'alexa': AlexaCollector,
            'windows': WindowsCollector,
            'mac': MacCollector
        }
        
        for name, config in enabled_collectors.items():
            if name in collector_classes:
                try:
                    collector = collector_classes[name](config)
                    if collector.validate_config():
                        self.collectors[name] = collector
                        self.logger.info(f"Initialized {name} collector")
                    else:
                        self.logger.warning(f"Invalid configuration for {name} collector")
                except Exception as e:
                    self.logger.error(f"Failed to initialize {name} collector: {e}")
            else:
                self.logger.warning(f"Unknown collector type: {name}")
        
        self.logger.info(f"Initialized {len(self.collectors)} collector(s)")
    
    def _connect_collectors(self) -> None:
        """Connect all initialized collectors."""
        self.logger.info("Connecting collectors...")
        
        for name, collector in self.collectors.items():
            try:
                if collector.connect():
                    self.logger.info(f"Connected {name} collector")
                else:
                    self.logger.warning(f"Failed to connect {name} collector")
            except Exception as e:
                self.logger.error(f"Error connecting {name} collector: {e}")
    
    def _disconnect_collectors(self) -> None:
        """Disconnect all collectors."""
        self.logger.info("Disconnecting collectors...")
        
        for name, collector in self.collectors.items():
            try:
                collector.disconnect()
                self.logger.info(f"Disconnected {name} collector")
            except Exception as e:
                self.logger.error(f"Error disconnecting {name} collector: {e}")
    
    def _collect_data_from_all(self) -> List[DeviceData]:
        """
        Collect data from all connected collectors.
        
        Returns:
            List of all collected DeviceData objects
        """
        all_data = []
        
        for name, collector in self.collectors.items():
            try:
                if collector.is_connected():
                    data = collector.collect_data()
                    all_data.extend(data)
                    self.logger.debug(f"Collected {len(data)} data point(s) from {name}")
                else:
                    self.logger.warning(f"{name} collector is not connected")
            except Exception as e:
                self.logger.error(f"Error collecting data from {name}: {e}")
        
        return all_data
    
    def _process_collected_data(self, data: List[DeviceData]) -> None:
        """
        Process and store collected data.
        
        Args:
            data: List of DeviceData objects to process
        """
        if not data:
            self.logger.debug("No data to process")
            return
        
        # TODO: Implement data storage (database, file, etc.)
        # For now, just log the data
        self.logger.info(f"Processing {len(data)} data point(s)")
        
        for item in data:
            self.logger.debug(f"Data: {item.device_name} - {item.data}")
    
    def run(self) -> None:
        """Run the main application loop."""
        self.logger.info("Starting Jarvis Home Automation System")
        
        # Initialize collectors
        self._initialize_collectors()
        
        if not self.collectors:
            self.logger.error("No collectors configured or initialized")
            return
        
        # Connect collectors
        self._connect_collectors()
        
        # Get collection interval
        collection_interval = self.config.get('data_collection.interval', 60)
        self.logger.info(f"Data collection interval: {collection_interval} seconds")
        
        self.running = True
        
        try:
            while self.running:
                start_time = time.time()
                
                # Collect data from all sources
                data = self._collect_data_from_all()
                
                # Process collected data
                self._process_collected_data(data)
                
                # Calculate sleep time
                elapsed = time.time() - start_time
                sleep_time = max(0, collection_interval - elapsed)
                
                if self.running and sleep_time > 0:
                    self.logger.debug(f"Sleeping for {sleep_time:.2f} seconds")
                    time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop the application."""
        self.logger.info("Stopping Jarvis Home Automation System")
        self.running = False
        self._disconnect_collectors()
        self.logger.info("Jarvis stopped")


def main():
    """Main entry point."""
    app = JarvisApp()
    app.run()


if __name__ == '__main__':
    main()
