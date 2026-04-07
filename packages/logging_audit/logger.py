import json
import logging
import datetime
from typing import Any, Dict

_STANDARD_LOG_KEYS = set(logging.makeLogRecord({}).__dict__.keys())

class JSONFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the LogRecord.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": datetime.datetime.fromtimestamp(record.created, tz=datetime.timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }

        # Include standard exception text if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Include any extra keys added to the log record
        # (excluding standard LogRecord attributes)
        extra_keys = set(record.__dict__.keys()) - _STANDARD_LOG_KEYS
        for key in extra_keys:
            log_record[key] = record.__dict__[key]

        return json.dumps(log_record, ensure_ascii=False)


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Returns a logger configured to output JSON formatted logs.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if get_logger is called multiple times for same name
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = JSONFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Prevent log messages from being propagated to the root logger
    logger.propagate = False

    return logger
