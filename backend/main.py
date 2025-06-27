"""
LLM Stock Analyst - FastAPI Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from loguru import logger

from routers import chat, valuation, powerbi
from models.schemas import ErrorResponse

# Initialize FastAPI app
app = FastAPI(
    title="LLM Stock Analyst API",
    description="An intelligent stock valuation chatbot powered by LLMs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501", 
        "http://127.0.0.1:8501",
        "https://finchanalytics-rag.streamlit.app",  # Deployed Streamlit frontend
        "https://finchanalytics-rag.streamlit.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(valuation.router, prefix="/api/v1", tags=["valuation"])
app.include_router(powerbi.router, prefix="/api/v1", tags=["powerbi"])

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("🚀 LLM Stock Analyst API starting up...")
    # TODO: Initialize database connections, API clients, etc.

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("🛑 LLM Stock Analyst API shutting down...")
    # TODO: Close database connections, cleanup resources

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LLM Stock Analyst API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "llm-stock-analyst"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            message="An unexpected error occurred"
        ).dict()
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 