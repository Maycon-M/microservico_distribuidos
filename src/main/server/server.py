from __future__ import annotations
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.core.logging_config import setup_logging, get_logger

from src.main.routes.users_routes import router as users_router
from src.main.routes.medicines_routes import router as medicines_router
from src.main.routes.reminders_routes import router as reminders_router

setup_logging()
logger = get_logger(__name__)
app = FastAPI(title="Dose Certa API", version="1.0.0")

ALLOWED_ORIGINS = ["*"]
ALLOWED_METHODS = ["GET", "POST", "OPTIONS"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=["*"],
)

@app.middleware(middleware_type="https")
async def log_requests(request: Request, call_next):
    logger.info("Recebendo requisição: %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error("Erro não tratado durante a requisição: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    logger.info("Respondendo requisição: %s %s -> Status %s", request.method, request.url.path, response.status_code)
    return response


# Routers
app.include_router(users_router)
app.include_router(medicines_router)
app.include_router(reminders_router)

@app.get("/health", tags=["Health"], summary="Health Check")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

