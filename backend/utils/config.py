"""
Configuration utilities for the LLM Stock Analyst application
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from loguru import logger

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # Power BI Configuration
    powerbi_client_id: Optional[str] = None
    powerbi_client_secret: Optional[str] = None
    powerbi_tenant_id: Optional[str] = None
    powerbi_workspace_id: Optional[str] = None
    
    # API Configuration
    backend_host: str = "localhost"
    backend_port: int = 8000
    frontend_port: int = 8501
    
    # Database Configuration
    database_url: str = "sqlite:///./data/stock_analyst.db"
    
    # Logging
    log_level: str = "INFO"
    
    # Security
    secret_key: str = "your-secret-key-change-this"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

def validate_configuration() -> bool:
    """
    Validate that all required configuration is present
    
    Returns:
        True if configuration is valid, False otherwise
    """
    missing_configs = []
    
    # Check required configurations
    if not settings.openai_api_key:
        missing_configs.append("OPENAI_API_KEY")
    
    # Power BI is optional but warn if partially configured
    powerbi_configs = [
        settings.powerbi_client_id,
        settings.powerbi_client_secret,
        settings.powerbi_tenant_id
    ]
    
    if any(powerbi_configs) and not all(powerbi_configs):
        logger.warning("Power BI partially configured - some features may not work")
    
    if missing_configs:
        logger.error(f"Missing required configuration: {', '.join(missing_configs)}")
        return False
    
    logger.info("Configuration validation passed")
    return True

def get_api_url() -> str:
    """Get the backend API URL"""
    return f"http://{settings.backend_host}:{settings.backend_port}"

def get_frontend_url() -> str:
    """Get the frontend URL"""
    return f"http://{settings.backend_host}:{settings.frontend_port}" 