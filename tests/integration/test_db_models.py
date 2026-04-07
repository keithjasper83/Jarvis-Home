import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infra.db.models import Base, Device, Capability

class TestDatabaseModels(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = self.SessionLocal()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_device(self):
        device = Device(
            friendly_name="Test Light",
            device_type="light",
            protocol="http",
            host="192.168.1.50"
        )
        self.session.add(device)
        self.session.commit()

        # Verify it was written and fields match
        saved_device = self.session.query(Device).filter_by(friendly_name="Test Light").first()
        self.assertIsNotNone(saved_device)
        self.assertEqual(saved_device.device_type, "light")
        self.assertEqual(saved_device.host, "192.168.1.50")
        self.assertTrue(saved_device.enabled) # defaults to True

    def test_create_capability(self):
        capability = Capability(
            capability_key="light.on",
            display_name="Turn Light On",
            category="lighting",
            safety_level="safe"
        )
        self.session.add(capability)
        self.session.commit()

        # Verify it was written
        saved_capability = self.session.query(Capability).filter_by(capability_key="light.on").first()
        self.assertIsNotNone(saved_capability)
        self.assertEqual(saved_capability.display_name, "Turn Light On")

if __name__ == "__main__":
    unittest.main()
