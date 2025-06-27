"""
LLM Stock Analyst - FastAPI Main Application (Simplified for deployment)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from loguru import logger

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

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("🚀 LLM Stock Analyst API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("🛑 LLM Stock Analyst API shutting down...")

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

@app.post("/api/v1/chat")
async def chat_endpoint(request: dict):
    """Simple chat endpoint for testing"""
    return {
        "response": "Hello! This is a simplified version of the LLM Stock Analyst. The full features are being deployed.",
        "stock_symbol": request.get("stock_symbol"),
        "confidence": 0.8,
        "sources": ["API Test"],
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/api/v1/valuation")
async def valuation_endpoint(request: dict):
    """Simple valuation endpoint for testing"""
    return {
        "stock_symbol": request.get("stock_symbol", "TEST"),
        "current_price": 100.0,
        "financial_metrics": {
            "current_price": 100.0,
            "market_cap": 1000000000.0,
            "pe_ratio": 15.0
        },
        "valuations": [
            {
                "method": "test",
                "estimated_value": 105.0,
                "confidence_interval": [95.0, 115.0],
                "assumptions": {"test": True},
                "calculation_details": {"note": "Simplified test version"}
            }
        ],
        "recommendation": "Hold - Test version",
        "risk_factors": ["This is a test deployment"],
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main-simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 