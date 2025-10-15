"""
WebSocket Routes for the WebSocket Broadcast System
"""

import json
import logging
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from connection_manager import ConnectionManager

logger = logging.getLogger(__name__)


def create_websocket_routes(manager: ConnectionManager) -> APIRouter:
    """Create WebSocket routes with the connection manager dependency"""
    
    router = APIRouter()

    @router.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """Main WebSocket endpoint for client connections"""
        await manager.connect(websocket)
        try:
            while True:
                # Listen for messages from the client
                data = await websocket.receive_text()
                await handle_websocket_message(data, manager)
                    
        except WebSocketDisconnect:
            manager.disconnect(websocket)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            manager.disconnect(websocket)

    @router.websocket("/ws/{client_id}")
    async def websocket_endpoint_with_id(websocket: WebSocket, client_id: str):
        """WebSocket endpoint with client ID for identification"""
        await manager.connect(websocket)
        
        # Send personalized welcome message
        welcome_msg = {
            "message": f"Welcome {client_id}! You are client #{manager.connection_count}",
            "sender": "System",
            "timestamp": datetime.now().isoformat(),
            "message_type": "welcome"
        }
        await websocket.send_text(json.dumps(welcome_msg))
        
        try:
            while True:
                # Listen for messages from the client
                data = await websocket.receive_text()
                await handle_websocket_message(data, manager, client_id)
                    
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            logger.info(f"Client {client_id} disconnected")
        except Exception as e:
            logger.error(f"WebSocket error for client {client_id}: {e}")
            manager.disconnect(websocket)

    return router


async def handle_websocket_message(data: str, manager: ConnectionManager, client_id: str = None):
    """Handle incoming WebSocket messages"""
    try:
        message_data = json.loads(data)
        
        # Determine sender name
        sender = client_id if client_id else message_data.get("sender", f"Client-{manager.connection_count}")
        
        # Create broadcast message
        broadcast_msg = {
            "message": message_data.get("message", data),
            "sender": sender,
            "timestamp": datetime.now().isoformat(),
            "message_type": message_data.get("message_type", "chat")
        }
        
        # Handle different message types
        msg_type = message_data.get("message_type", "broadcast")
        
        if msg_type == "ping":
            # Handle ping messages - send pong back
            pong_msg = {
                "message": "pong",
                "sender": "System",
                "timestamp": datetime.now().isoformat(),
                "message_type": "pong"
            }
            # This would need the specific websocket, so we broadcast it
            await manager.broadcast(pong_msg)
        elif msg_type == "private":
            # Handle private messages (this is a placeholder for future implementation)
            logger.info(f"Private message from {sender}: {message_data.get('message')}")
        else:
            # Regular broadcast message
            await manager.broadcast(broadcast_msg)
            
    except json.JSONDecodeError:
        # If it's not JSON, treat as plain text
        sender = client_id if client_id else f"Client-{manager.connection_count}"
        broadcast_msg = {
            "message": data,
            "sender": sender,
            "timestamp": datetime.now().isoformat(),
            "message_type": "chat"
        }
        await manager.broadcast(broadcast_msg)
    except Exception as e:
        logger.error(f"Error handling WebSocket message: {e}")