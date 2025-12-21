"""
Basic tests for Jarvis collectors
"""

import unittest
from src.jarvis.data_collectors.base_collector import BaseCollector
from src.jarvis.data_collectors.shelly_collector import ShellyCollector
from src.jarvis.data_collectors.tapo_collector import TapoCollector
from src.jarvis.data_collectors.alexa_collector import AlexaCollector
from src.jarvis.data_collectors.windows_collector import WindowsCollector
from src.jarvis.data_collectors.mac_collector import MacCollector


class TestCollectorInstantiation(unittest.TestCase):
    """Test cases for collector instantiation."""
    
    def test_shelly_collector_creation(self):
        """Test creating a Shelly collector."""
        config = {
            'api_key': 'test_key',
            'devices': [],
            'poll_interval': 60
        }
        collector = ShellyCollector(config)
        
        self.assertEqual(collector.name, 'shelly')
        self.assertFalse(collector.is_connected())
    
    def test_tapo_collector_creation(self):
        """Test creating a Tapo collector."""
        config = {
            'username': 'test_user',
            'password': 'test_pass',
            'devices': []
        }
        collector = TapoCollector(config)
        
        self.assertEqual(collector.name, 'tapo')
        self.assertFalse(collector.is_connected())
    
    def test_alexa_collector_creation(self):
        """Test creating an Alexa collector."""
        config = {
            'access_token': 'test_token',
            'devices': []
        }
        collector = AlexaCollector(config)
        
        self.assertEqual(collector.name, 'alexa')
        self.assertFalse(collector.is_connected())
    
    def test_windows_collector_creation(self):
        """Test creating a Windows collector."""
        config = {
            'host': 'localhost',
            'collect_processes': False,
            'collect_network': True
        }
        collector = WindowsCollector(config)
        
        self.assertEqual(collector.name, 'windows')
        self.assertFalse(collector.is_connected())
    
    def test_mac_collector_creation(self):
        """Test creating a Mac collector."""
        config = {
            'host': 'localhost',
            'collect_processes': False,
            'collect_network': True
        }
        collector = MacCollector(config)
        
        self.assertEqual(collector.name, 'mac')
        self.assertFalse(collector.is_connected())


if __name__ == '__main__':
    unittest.main()
