import contextvars
import uuid

# ContextVar to store the request_id for the current task
request_id_var = contextvars.ContextVar("request_id", default=None)

def get_request_id() -> str:
    return request_id_var.get()

def set_request_id(request_id: str):
    request_id_var.set(request_id)
