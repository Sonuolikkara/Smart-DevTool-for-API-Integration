from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from backend.config import settings
from backend.routes import documents, analysis, generation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Smart DevTool API starting...")
    yield
    logger.info("🛑 Smart DevTool API shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="Smart DevTool for API Integration",
    description="Auto-generate SDK wrappers from API documentation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(generation.router, prefix="/api/generation", tags=["generation"])


@app.get("/", tags=["health"])
async def root():
    """Root endpoint - API information"""
    return {
        "service": "Smart DevTool for API Integration",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Smart DevTool API",
        "version": "1.0.0"
    }


@app.post("/api/analyze", tags=["analysis"])
async def analyze_api(url: str = None, documentation: str = None):
    """
    Analyze API documentation and extract endpoints
    
    Will be fully implemented on Day 2
    """
    if not url and not documentation:
        raise HTTPException(
            status_code=400,
            detail="Either 'url' or 'documentation' must be provided"
        )
    
    return {
        "status": "pending",
        "message": "Analysis endpoint - implementation coming Day 2",
        "input": {
            "url": url,
            "has_documentation": documentation is not None
        }
    }


@app.post("/api/generate", tags=["generation"])
async def generate_code(
    endpoints: list = None,
    auth_method: dict = None,
    language: str = "python"
):
    """
    Generate wrapper code from extracted endpoints
    
    Will be fully implemented on Day 5
    """
    return {
        "status": "pending",
        "message": "Code generation endpoint - implementation coming Day 5",
        "configuration": {
            "language": language,
            "endpoint_count": len(endpoints) if endpoints else 0,
            "auth_configured": auth_method is not None
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
