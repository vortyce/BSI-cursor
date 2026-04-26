import logging
import json
from app.core.context import get_request_id

class StructuredLogger:
    def __init__(self, domain: str):
        self.domain = domain
        self.logger = logging.getLogger(f"bsi.{domain}")

    def _format(self, level: str, action: str, message: str, error_context: dict = None):
        log_data = {
            "level": level,
            "domain": self.domain,
            "action": action,
            "request_id": get_request_id(),
            "message": message
        }
        if error_context:
            log_data["error_context"] = error_context
        return json.dumps(log_data)

    def info(self, action: str, message: str):
        self.logger.info(self._format("INFO", action, message))

    def error(self, action: str, message: str, error_context: dict = None):
        self.logger.error(self._format("ERROR", action, message, error_context))

    def warning(self, action: str, message: str):
        self.logger.warning(self._format("WARNING", action, message))

def get_logger(domain: str) -> StructuredLogger:
    return StructuredLogger(domain)
