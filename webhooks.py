"""
Webhook Definitions for the WebSocket Broadcast System
"""

from fastapi import FastAPI

from models import BroadcastMessage, WebhookNotification


def setup_webhooks(app: FastAPI):
    """Setup webhook definitions for the FastAPI app"""
    
    @app.webhooks.post("message-broadcast")
    def message_broadcast_webhook(body: BroadcastMessage):
        """
        When a message needs to be broadcasted to all connected clients,
        we'll send you a POST request with this data to the URL that you register 
        for the event `message-broadcast` in your webhook configuration.
        
        This webhook is triggered when:
        - A new message is broadcasted via the REST API
        - A message is sent through WebSocket that gets broadcasted
        """
        pass

    @app.webhooks.post("client-connected")
    def client_connected_webhook(body: WebhookNotification):
        """
        Triggered when a new client connects to the WebSocket.
        
        The notification body will contain:
        - event_type: "client_connected"
        - data: {"client_number": int, "total_connections": int}
        - timestamp: ISO format datetime
        """
        pass

    @app.webhooks.post("client-disconnected")
    def client_disconnected_webhook(body: WebhookNotification):
        """
        Triggered when a client disconnects from the WebSocket.
        
        The notification body will contain:
        - event_type: "client_disconnected" 
        - data: {"remaining_connections": int}
        - timestamp: ISO format datetime
        """
        pass

    @app.webhooks.post("server-status")
    def server_status_webhook(body: WebhookNotification):
        """
        Triggered for server status updates like startup, shutdown, or health changes.
        
        The notification body will contain:
        - event_type: "server_startup" | "server_shutdown" | "health_check"
        - data: {"status": str, "additional_info": dict}
        - timestamp: ISO format datetime
        """
        pass

    @app.webhooks.post("broadcast-stats")
    def broadcast_stats_webhook(body: WebhookNotification):
        """
        Triggered periodically with broadcast statistics.
        
        The notification body will contain:
        - event_type: "stats_update"
        - data: {"active_connections": int, "total_messages": int, "uptime": int}
        - timestamp: ISO format datetime
        """
        pass