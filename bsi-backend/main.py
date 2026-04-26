from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.webhooks import router as webhook_router
from app.api.v1.interpretations import router as interpretation_router
from app.api.v1.outcomes import router as outcome_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.system import router as system_router
from app.api.v1.portfolio import router as portfolio_router
from app.core.config import settings
from app.core.errors import ServiceError
from app.schemas.response import StandardResponse
from app.core.response_utils import to_compatible_response

from app.core.middleware import RequestIDMiddleware

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Configuração de Middleware de Correlação
app.add_middleware(RequestIDMiddleware)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ServiceError)
async def service_error_handler(request: Request, exc: ServiceError):
    res = StandardResponse.error_response(
        code=exc.code,
        message=exc.message,
        domain=exc.domain,
        details=exc.details,
    )
    return JSONResponse(status_code=exc.status_code, content=to_compatible_response(res, legacy=False))

# Rotas
app.include_router(webhook_router, prefix="/api/v1/webhooks", tags=["Webhooks"])
app.include_router(interpretation_router, prefix="/api/v1/interpretations", tags=["Interpretations"])
app.include_router(outcome_router, prefix="/api/v1/outcomes", tags=["Outcomes"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(system_router, prefix="/api/v1/system", tags=["System"])
app.include_router(portfolio_router, prefix="/api/v1/portfolio", tags=["Portfolio"])

@app.get("/health")
def health_check():
    data = {
        "status": "healthy",
        "app": settings.APP_NAME,
        "mode": settings.ENVIRONMENT_MODE
    }
    res = StandardResponse.success_response(data=data, domain="system")
    return to_compatible_response(res)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
