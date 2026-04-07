import unittest
import logging
import json
from io import StringIO
from packages.logging_audit.logger import get_logger

class TestLogger(unittest.TestCase):
    def test_json_formatter(self):
        # We need to capture the output
        log_stream = StringIO()

        # Setup logger
        logger = get_logger("test_logger")

        # We need to replace the stream handler to write to our StringIO
        for handler in list(logger.handlers):
            logger.removeHandler(handler)

        handler = logging.StreamHandler(log_stream)
        from packages.logging_audit.logger import JSONFormatter
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

        # Log a test message
        logger.info("Test message", extra={"correlation_id": "12345"})

        # Get output
        output = log_stream.getvalue().strip()

        # Verify JSON
        log_dict = json.loads(output)
        self.assertEqual(log_dict["message"], "Test message")
        self.assertEqual(log_dict["level"], "INFO")
        self.assertEqual(log_dict["name"], "test_logger")
        self.assertEqual(log_dict["correlation_id"], "12345")
        self.assertIn("timestamp", log_dict)

if __name__ == "__main__":
    unittest.main()
