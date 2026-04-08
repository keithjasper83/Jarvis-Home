import unittest
from fastapi.testclient import TestClient
from apps.api.routes import app

class TestApiRoutes(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy", "version": "0.1.0"})

    def test_dashboard_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        # Check if Jinja2 processed the template variables
        self.assertIn("Jarvis Home", response.text)
        self.assertIn("Llama 3 8B", response.text)
        # Check for Tailwind/HTMX/Alpine presence
        self.assertIn("cdn.tailwindcss.com", response.text)
        self.assertIn("htmx.org", response.text)

if __name__ == "__main__":
    unittest.main()
