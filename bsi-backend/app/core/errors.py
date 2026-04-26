from typing import Any, Dict, Optional


class ServiceError(Exception):
    status_code = 500
    code = "SERVICE_ERROR"
    domain = "general"

    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        domain: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code or self.code
        self.domain = domain or self.domain
        self.details = details or {}


class NotFoundError(ServiceError):
    status_code = 404
    code = "NOT_FOUND"


class ValidationError(ServiceError):
    status_code = 400
    code = "VALIDATION_ERROR"


class BusinessRuleError(ServiceError):
    status_code = 400
    code = "BUSINESS_RULE_ERROR"
