"""
Basic tests for Jarvis data models
"""

import unittest
from datetime import datetime
from src.jarvis.models.device_data import DeviceData


class TestDeviceData(unittest.TestCase):
    """Test cases for DeviceData model."""
    
    def test_device_data_creation(self):
        """Test creating a DeviceData instance."""
        data = DeviceData(
            device_id='test_device_1',
            device_type='test',
            device_name='Test Device',
            data={'key': 'value'},
            status='online'
        )
        
        self.assertEqual(data.device_id, 'test_device_1')
        self.assertEqual(data.device_type, 'test')
        self.assertEqual(data.device_name, 'Test Device')
        self.assertEqual(data.status, 'online')
        self.assertIsInstance(data.timestamp, datetime)
    
    def test_device_data_to_dict(self):
        """Test converting DeviceData to dictionary."""
        data = DeviceData(
            device_id='test_device_1',
            device_type='test',
            device_name='Test Device',
            data={'key': 'value'},
            status='online'
        )
        
        data_dict = data.to_dict()
        
        self.assertIn('device_id', data_dict)
        self.assertIn('device_type', data_dict)
        self.assertIn('device_name', data_dict)
        self.assertIn('timestamp', data_dict)
        self.assertIn('data', data_dict)
        self.assertIn('status', data_dict)
        self.assertEqual(data_dict['device_id'], 'test_device_1')
    
    def test_device_data_from_dict(self):
        """Test creating DeviceData from dictionary."""
        data_dict = {
            'device_id': 'test_device_1',
            'device_type': 'test',
            'device_name': 'Test Device',
            'timestamp': datetime.now().isoformat(),
            'data': {'key': 'value'},
            'status': 'online',
            'metadata': {}
        }
        
        data = DeviceData.from_dict(data_dict)
        
        self.assertEqual(data.device_id, 'test_device_1')
        self.assertEqual(data.device_type, 'test')
        self.assertIsInstance(data.timestamp, datetime)


if __name__ == '__main__':
    unittest.main()
