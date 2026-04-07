import os
import unittest
from packages.configuration.settings import get_settings, Settings

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        # Save original environ
        self.original_env = dict(os.environ)

    def tearDown(self):
        # Restore original environ
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_default_settings(self):
        os.environ.clear()
        settings = get_settings()
        self.assertEqual(settings.system.environment, "development")
        self.assertTrue(settings.system.debug)
        self.assertEqual(settings.api.host, "0.0.0.0")
        self.assertEqual(settings.api.port, 8000)
        self.assertEqual(settings.db.url, "sqlite:///./local_prototype.db")

    def test_env_override_settings(self):
        os.environ["APP_ENV"] = "production"
        os.environ["APP_DEBUG"] = "false"
        os.environ["API_PORT"] = "9000"

        settings = get_settings()
        self.assertEqual(settings.system.environment, "production")
        self.assertFalse(settings.system.debug)
        self.assertEqual(settings.api.port, 9000)

if __name__ == "__main__":
    unittest.main()
