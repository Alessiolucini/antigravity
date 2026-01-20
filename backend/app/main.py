"""
Pronto Casa - Main FastAPI Application

Entry point for the Pronto Casa backend API.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.api.v1 import auth, requests, technicians, payments, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup application resources."""
    await init_db()
    yield


app = FastAPI(
    title="Pronto Casa API",
    description="API per la piattaforma di riparazioni urgenti a domicilio",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticazione"])
app.include_router(requests.router, prefix="/api/v1/requests", tags=["Richieste"])
app.include_router(technicians.router, prefix="/api/v1/technicians", tags=["Tecnici"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Pagamenti"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "pronto-casa-api"}


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Pronto Casa API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
