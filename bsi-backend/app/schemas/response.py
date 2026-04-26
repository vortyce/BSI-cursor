from typing import Any, Optional, Dict, Generic, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime
from app.core.context import get_request_id

T = TypeVar("T")

class ErrorModel(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = Field(default_factory=dict)

class ResponseMeta(BaseModel):
    request_id: Optional[str] = Field(default_factory=get_request_id)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    domain: str = "general"

class StandardResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ErrorModel] = None
    meta: ResponseMeta

    @classmethod
    def success_response(cls, data: T, domain: str = "general") -> "StandardResponse[T]":
        return cls(
            success=True,
            data=data,
            meta=ResponseMeta(domain=domain)
        )

    @classmethod
    def error_response(cls, code: str, message: str, domain: str = "general", details: Dict[str, Any] = None) -> "StandardResponse[None]":
        return cls(
            success=False,
            error=ErrorModel(code=code, message=message, details=details),
            meta=ResponseMeta(domain=domain)
        )
