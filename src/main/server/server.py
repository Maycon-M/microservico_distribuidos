from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.main.routes.users_routes import router as users_router
from src.main.routes.medicines_routes import router as medicines_router
from src.main.routes.reminders_routes import router as reminders_router


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

# Routers
app.include_router(users_router)
app.include_router(medicines_router)
app.include_router(reminders_router)

@app.get("/health", tags=["Health"], summary="Health Check")
def health():
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

