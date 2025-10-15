"""
API Routes for the WebSocket Broadcast System
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from models import BroadcastMessage, ConnectionStats
from connection_manager import ConnectionManager

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


def create_api_routes(manager: ConnectionManager) -> APIRouter:
    """Create API routes with the connection manager dependency"""
    
    @router.post("/broadcast", response_model=Dict[str, Any])
    async def broadcast_message(message: BroadcastMessage, background_tasks: BackgroundTasks):
        """
        Broadcast a message to all connected WebSocket clients via REST API
        """
        if message.timestamp is None:
            message.timestamp = datetime.now()
        
        broadcast_data = {
            "message": message.message,
            "sender": message.sender,
            "timestamp": message.timestamp.isoformat(),
            "message_type": message.message_type
        }
        
        success = await manager.broadcast(broadcast_data)
        
        if not success:
            raise HTTPException(status_code=503, detail="No active connections to broadcast to")
        
        return {
            "status": "success",
            "message": "Message broadcasted successfully",
            "active_connections": len(manager.active_connections),
            "broadcast_data": broadcast_data
        }

    @router.post("/broadcast/specific", response_model=Dict[str, Any])
    async def broadcast_to_specific(
        message: BroadcastMessage, 
        client_indices: list[int],
        background_tasks: BackgroundTasks
    ):
        """
        Broadcast a message to specific clients by their connection indices
        """
        if message.timestamp is None:
            message.timestamp = datetime.now()
        
        broadcast_data = {
            "message": message.message,
            "sender": message.sender,
            "timestamp": message.timestamp.isoformat(),
            "message_type": message.message_type
        }
        
        success = await manager.broadcast_to_specific_clients(broadcast_data, client_indices)
        
        if not success:
            raise HTTPException(
                status_code=503, 
                detail="Could not send message to any of the specified clients"
            )
        
        return {
            "status": "success",
            "message": f"Message sent to {len(client_indices)} specific clients",
            "target_clients": client_indices,
            "broadcast_data": broadcast_data
        }

    @router.get("/stats", response_model=ConnectionStats)
    async def get_connection_stats():
        """
        Get current connection statistics
        """
        return manager.get_stats()

    @router.get("/info", response_model=Dict[str, Any])
    async def get_connection_info():
        """
        Get detailed connection information
        """
        return manager.get_connection_info()

    @router.get("/health")
    async def health_check():
        """
        Health check endpoint
        """
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "active_connections": len(manager.active_connections),
            "server_info": {
                "name": "WebSocket Broadcast System",
                "version": "1.0.0"
            }
        }

    @router.get("/")
    async def get_test_page():
        """
        Serve the HTML test page
        """
        return FileResponse("templates/index.html")

    return router