"""
REST API Client Example

This script demonstrates how to interact with the broadcast server
using REST API endpoints.
"""

import requests
import json
from datetime import datetime
import time

class RestApiClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def send_broadcast(self, message: str, sender: str = "REST Client", message_type: str = "broadcast"):
        """Send a broadcast message via REST API"""
        url = f"{self.base_url}/broadcast"
        
        data = {
            "message": message,
            "sender": sender,
            "message_type": message_type
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Broadcast sent successfully!")
            print(f"   Active connections: {result['active_connections']}")
            print(f"   Message: {result['broadcast_data']['message']}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending broadcast: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"   Server error: {error_detail}")
                except:
                    print(f"   Server response: {e.response.text}")
            return None

    def get_stats(self):
        """Get server statistics"""
        url = f"{self.base_url}/stats"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            stats = response.json()
            print("\n📊 Server Statistics:")
            print(f"   Active connections: {stats['active_connections']}")
            print(f"   Total messages sent: {stats['total_messages_sent']}")
            print(f"   Uptime: {stats['uptime_seconds']} seconds")
            return stats
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting stats: {e}")
            return None

    def health_check(self):
        """Check server health"""
        url = f"{self.base_url}/health"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            health = response.json()
            print(f"💚 Server is healthy")
            print(f"   Status: {health['status']}")
            print(f"   Timestamp: {health['timestamp']}")
            print(f"   Active connections: {health['active_connections']}")
            return health
        except requests.exceptions.RequestException as e:
            print(f"❌ Server health check failed: {e}")
            return None

def interactive_rest_client():
    """Interactive REST API client"""
    client = RestApiClient()
    
    print("REST API Client for WebSocket Broadcast Server")
    print("Commands:")
    print("  'send <message>' - Send a broadcast message")
    print("  'stats' - Get server statistics")
    print("  'health' - Check server health")
    print("  'demo' - Run automated demo")
    print("  'quit' - Exit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("Enter command: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'stats':
                client.get_stats()
            elif user_input.lower() == 'health':
                client.health_check()
            elif user_input.lower() == 'demo':
                run_demo(client)
            elif user_input.startswith('send '):
                message = user_input[5:]  # Remove 'send ' prefix
                if message:
                    client.send_broadcast(message, "Interactive User")
                else:
                    print("Please provide a message to send")
            elif user_input.lower() == 'help':
                print("\nCommands:")
                print("  'send <message>' - Send a broadcast message")
                print("  'stats' - Get server statistics")
                print("  'health' - Check server health")
                print("  'demo' - Run automated demo")
                print("  'quit' - Exit")
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def run_demo(client):
    """Run automated demo"""
    print("\n🚀 Starting REST API Demo...")
    
    # Health check
    client.health_check()
    print()
    
    # Get initial stats
    client.get_stats()
    print()
    
    # Send multiple broadcast messages
    messages = [
        "Welcome to the REST API demo!",
        "This message is sent via HTTP POST",
        "All connected WebSocket clients will receive this",
        "Demo message #4 with timestamp: " + datetime.now().strftime("%H:%M:%S"),
        "Final demo message - Thanks for watching!"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n📤 Sending message {i}/{len(messages)}:")
        client.send_broadcast(message, f"Demo Bot #{i}")
        time.sleep(2)  # Wait 2 seconds between messages
    
    print("\n🎉 Demo completed!")
    
    # Get final stats
    print()
    client.get_stats()

def main():
    print("REST API Client Demo")
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print()
    
    # Test connection first
    client = RestApiClient()
    if client.health_check():
        print()
        interactive_rest_client()
    else:
        print("\n❌ Cannot connect to server. Make sure it's running on http://localhost:8000")
        print("Start the server with: python main.py")

if __name__ == "__main__":
    main()