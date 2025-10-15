"""
Pydantic models for the WebSocket Broadcast System
"""

from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, Field


class BroadcastMessage(BaseModel):
    """Model for broadcast messages"""
    message: str = Field(..., description="The message content to broadcast")
    sender: str = Field(default="System", description="The sender of the message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the message")
    message_type: str = Field(default="broadcast", description="Type of the message")


class WebhookNotification(BaseModel):
    """Model for webhook notifications"""
    event_type: str = Field(..., description="Type of the event")
    data: Dict[str, Any] = Field(..., description="Event data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the event")


class ConnectionStats(BaseModel):
    """Model for connection statistics"""
    active_connections: int = Field(..., description="Number of active WebSocket connections")
    total_messages_sent: int = Field(..., description="Total number of messages sent")
    uptime_seconds: int = Field(..., description="Server uptime in seconds")


class ChatMessage(BaseModel):
    """Model for chat messages from WebSocket clients"""
    message: str = Field(..., description="The chat message content")
    sender: str = Field(default="Anonymous", description="The sender's name")
    message_type: str = Field(default="chat", description="Type of the message")