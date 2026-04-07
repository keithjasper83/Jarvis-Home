import os
import unittest
from packages.configuration.settings import get_settings

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        # Save original environ
        self.original_env = dict(os.environ)

    def tearDown(self):
        # Restore original environ
        os.environ.clear()
        os.environ.update(self.original_env)

    def _clear_app_env_vars(self):
        for key in ["APP_ENV", "APP_DEBUG", "API_HOST", "API_PORT", "DATABASE_URL"]:
            if key in os.environ:
                del os.environ[key]

    def test_default_settings(self):
        self._clear_app_env_vars()
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
        os.environ["API_HOST"] = "127.0.0.1"
        os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost:5432/app"

        settings = get_settings()

        self.assertEqual(settings.system.environment, "production")
        self.assertFalse(settings.system.debug)
        self.assertEqual(settings.api.port, 9000)
        self.assertEqual(settings.api.host, "127.0.0.1")
        self.assertEqual(settings.db.url, "postgresql://user:pass@localhost:5432/app")

if __name__ == "__main__":
    unittest.main()
