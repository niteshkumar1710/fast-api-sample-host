## Installation

1. **Clone or create the project directory:**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### 1. Start the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### 2. Access the Web Interface

Open your browser and go to: `http://localhost:8000`

The web interface provides:
- Real-time WebSocket connection
- Message sending and receiving
- Connection statistics
- REST API testing interface

### 3. API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Client Examples

### WebSocket Client
```bash
python client_example.py
```

Choose between:
1. **Interactive client**: Manual message sending
2. **Automated demo**: Programmatic message broadcasting

### REST API Client
```bash
python rest_client_example.py
```

Features:
- Interactive command-line interface
- Health checks and statistics
- Automated demo mode

## Webhook Integration

The application defines OpenAPI webhooks for external integrations:

### Available Webhooks

1. **message-broadcast**: Triggered when broadcasting messages
2. **client-connected**: Triggered when a client connects
3. **client-disconnected**: Triggered when a client disconnects

### Webhook Configuration

Webhooks are documented in the OpenAPI schema and can be viewed at `/docs`. External systems can register URLs to receive webhook notifications.

## Message Types

The system supports different message types:

- `welcome`: System welcome messages for new connections
- `chat`: User-generated messages from WebSocket clients
- `broadcast`: System broadcast messages
- `api_broadcast`: Messages sent via REST API

## Connection Management

The `ConnectionManager` class handles:
- WebSocket connection lifecycle
- Message broadcasting to all clients
- Connection statistics tracking
- Automatic cleanup of disconnected clients

## Configuration

### Default Settings
- **Host**: `0.0.0.0` (all interfaces)
- **Port**: `8000`
- **Reload**: `True` (development mode)

### Customizing the Server

Modify the `uvicorn.run()` call in `main.py`:

```python
uvicorn.run(
    "main:app", 
    host="0.0.0.0", 
    port=8000,  # Change port here
    reload=True,
    log_level="info"
)
```