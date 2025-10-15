"""
WebSocket Connection Manager for handling client connections and broadcasting
"""

import json
import logging
from datetime import datetime
from typing import List, Dict, Any

from fastapi import WebSocket

from models import ConnectionStats

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections and broadcasting"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_count = 0
        self.total_messages_sent = 0
        self.start_time = datetime.now()

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_count += 1
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
        
        # Send welcome message to the new client
        welcome_msg = {
            "message": f"Welcome! You are client #{self.connection_count}",
            "sender": "System",
            "timestamp": datetime.now().isoformat(),
            "message_type": "welcome"
        }
        await websocket.send_text(json.dumps(welcome_msg))

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a personal message to a specific client"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: Dict[str, Any]) -> bool:
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            logger.warning("No active connections to broadcast to")
            return False

        message_text = json.dumps(message)
        disconnected_clients = []

        for connection in self.active_connections:
            try:
                await connection.send_text(message_text)
                self.total_messages_sent += 1
            except Exception as e:
                logger.error(f"Error sending message to client: {e}")
                disconnected_clients.append(connection)

        # Remove disconnected clients
        for client in disconnected_clients:
            self.disconnect(client)

        logger.info(f"Broadcasted message to {len(self.active_connections)} clients")
        return True

    async def broadcast_to_specific_clients(self, message: Dict[str, Any], client_indices: List[int]) -> bool:
        """Broadcast message to specific clients by their connection index"""
        if not self.active_connections:
            logger.warning("No active connections available")
            return False

        message_text = json.dumps(message)
        sent_count = 0
        disconnected_clients = []

        for index in client_indices:
            if 0 <= index < len(self.active_connections):
                connection = self.active_connections[index]
                try:
                    await connection.send_text(message_text)
                    self.total_messages_sent += 1
                    sent_count += 1
                except Exception as e:
                    logger.error(f"Error sending message to client {index}: {e}")
                    disconnected_clients.append(connection)

        # Remove disconnected clients
        for client in disconnected_clients:
            self.disconnect(client)

        logger.info(f"Sent message to {sent_count} specific clients")
        return sent_count > 0

    def get_stats(self) -> ConnectionStats:
        """Get current connection statistics"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        return ConnectionStats(
            active_connections=len(self.active_connections),
            total_messages_sent=self.total_messages_sent,
            uptime_seconds=int(uptime)
        )

    def get_connection_info(self) -> Dict[str, Any]:
        """Get detailed connection information"""
        return {
            "active_connections": len(self.active_connections),
            "total_connections_created": self.connection_count,
            "total_messages_sent": self.total_messages_sent,
            "start_time": self.start_time.isoformat(),
            "uptime_seconds": int((datetime.now() - self.start_time).total_seconds())
        }