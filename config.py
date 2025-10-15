"""
Configuration settings for the WebSocket Broadcast System
"""

import os
from typing import Optional


class Settings:
    """Application settings"""
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "true").lower() == "true"
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # Application settings
    APP_NAME: str = "WebSocket Broadcast System"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A FastAPI application for broadcasting messages to WebSocket clients with webhook support"
    
    # WebSocket settings
    MAX_CONNECTIONS: Optional[int] = int(os.getenv("MAX_CONNECTIONS", "100")) if os.getenv("MAX_CONNECTIONS") else None
    HEARTBEAT_INTERVAL: int = int(os.getenv("HEARTBEAT_INTERVAL", "30"))  # seconds
    
    # Message settings
    MAX_MESSAGE_SIZE: int = int(os.getenv("MAX_MESSAGE_SIZE", "1024"))  # bytes
    MESSAGE_QUEUE_SIZE: int = int(os.getenv("MESSAGE_QUEUE_SIZE", "100"))
    
    # Static files
    STATIC_DIR: str = os.getenv("STATIC_DIR", "static")
    TEMPLATES_DIR: str = os.getenv("TEMPLATES_DIR", "templates")
    
    # CORS settings
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    CORS_METHODS: list = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_HEADERS: list = ["*"]


# Global settings instance
settings = Settings()