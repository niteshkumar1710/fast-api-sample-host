"""
FastAPI WebSocket Broadcast System

This application provides:
1. WebSocket connections for real-time communication
2. Broadcast messages to all connected clients
3. REST API endpoints for sending broadcast messages
4. Webhook support for external notifications
5. Simple web interface for testing
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import local modules
from config import settings
from connection_manager import ConnectionManager
from api_routes import create_api_routes
from websocket_routes import create_websocket_routes
from webhooks import setup_webhooks

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper()))
logger = logging.getLogger(__name__)

# Initialize connection manager
manager = ConnectionManager()

# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI WebSocket Broadcast Server starting up...")
    yield
    logger.info("FastAPI WebSocket Broadcast Server shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    # Initialize FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )

    # Setup webhook definitions
    setup_webhooks(app)

    # Include API routes
    api_router = create_api_routes(manager)
    app.include_router(api_router)

    # Include WebSocket routes
    websocket_router = create_websocket_routes(manager)
    app.include_router(websocket_router)

    return app


# Create the app instance
app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL
    )