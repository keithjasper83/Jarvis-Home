import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infra.db.models import Base
from packages.device_registry.registry import DeviceRegistry

class TestDeviceRegistry(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = self.SessionLocal()
        self.registry = DeviceRegistry(self.session)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_and_get_device(self):
        device = self.registry.create_device({
            "friendly_name": "Kitchen Light",
            "device_type": "light",
            "host": "192.168.1.51"
        })
        self.assertIsNotNone(device.id)

        fetched = self.registry.get_device(device.id)
        self.assertEqual(fetched.friendly_name, "Kitchen Light")
        self.assertEqual(fetched.host, "192.168.1.51")

    def test_list_and_filter_devices(self):
        self.registry.create_device({"friendly_name": "Kitchen Light", "room": "kitchen", "device_type": "light"})
        self.registry.create_device({"friendly_name": "Kitchen Speaker", "room": "kitchen", "device_type": "speaker"})
        self.registry.create_device({"friendly_name": "Living Room TV", "room": "living_room", "device_type": "tv"})

        kitchen_devices = self.registry.list_devices({"room": "kitchen"})
        self.assertEqual(len(kitchen_devices), 2)

        lights = self.registry.list_devices({"device_type": "light"})
        self.assertEqual(len(lights), 1)

    def test_update_and_delete_device(self):
        device = self.registry.create_device({"friendly_name": "Kitchen Light", "room": "kitchen"})
        self.registry.update_device(device.id, {"room": "hallway", "enabled": False})

        fetched = self.registry.get_device(device.id)
        self.assertEqual(fetched.room, "hallway")
        self.assertFalse(fetched.enabled)

        self.assertTrue(self.registry.delete_device(device.id))
        self.assertIsNone(self.registry.get_device(device.id))

if __name__ == "__main__":
    unittest.main()
