import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.context import set_request_id

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Reutiliza X-Request-ID se enviado pelo cliente, senão gera UUID
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # 2. Injeta no contexto para ser usado por logs e serviços
        set_request_id(request_id)
        
        # 3. Processa a requisição
        response = await call_next(request)
        
        # 4. Injeta o request_id no header da response (boa prática para o cliente)
        response.headers["X-Request-ID"] = request_id
        
        return response
