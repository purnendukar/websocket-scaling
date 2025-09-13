# WebSocket Scaling with Redis and Nginx

A demonstration project showing how to scale WebSocket applications using Nginx as a load balancer and Redis for message distribution between multiple server instances.

## Architecture

This project consists of:

- **2 WebSocket Servers**: Python-based WebSocket servers using the `websockets` library
- **Redis**: Message broker for pub/sub communication between servers  
- **Nginx**: Load balancer distributing WebSocket connections across servers

The setup ensures that messages sent to any server instance are broadcast to all connected clients across all servers through Redis pub/sub.

## Features

- Load balancing WebSocket connections using Nginx
- Message broadcasting across multiple server instances via Redis
- Docker containerized deployment
- Configurable server ports and names

## Prerequisites

- Docker
- Docker Compose

## Project Structure

```
SocketScaling/
├── docker-compose.yml          # Multi-container orchestration
├── nginx/
│   └── nginx.conf             # Load balancer configuration
├── server/
│   ├── Dockerfile             # Server container definition
│   ├── server.py              # WebSocket server implementation
│   └── __init__.py
├── pyproject.toml             # Python project metadata
└── README.md                  # This file
```

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/purnendukar/websocket-scaling.git
   cd SocketScaling
   ```

2. Start the services:
   ```bash
   docker-compose up --build
   ```

3. Connect to the WebSocket endpoint:
   - URL: `ws://localhost:8085`
   - Nginx will load balance connections between Server-1 (port 8001) and Server-2 (port 8002)

4. Test the scaling:
   - Connect multiple WebSocket clients to `ws://localhost:8085`
   - Send messages from any client - they will be broadcast to all connected clients across both servers

## Configuration

### Environment Variables

Each server can be configured with:
- `PORT`: Server port (default: 8001)
- `SERVER_NAME`: Display name for the server instance

### Ports

- `8085`: Nginx load balancer (external access)
- `6380`: Redis (external access for debugging)
- `8001`, `8002`: WebSocket servers (internal)

## How It Works

1. **Client Connection**: Clients connect to `ws://localhost:8085`
2. **Load Balancing**: Nginx distributes connections between Server-1 and Server-2
3. **Message Handling**: When a server receives a message, it publishes it to Redis
4. **Broadcasting**: All servers subscribe to Redis and broadcast messages to their connected clients
5. **Scaling**: Messages are delivered to all clients regardless of which server they're connected to

## Development

To modify the WebSocket server logic, edit `server/server.py`. The server handles:
- WebSocket connection management
- Redis pub/sub for message distribution
- Message broadcasting to connected clients

To adjust load balancing, modify `nginx/nginx.conf`. Currently uses round-robin distribution.

## Testing

You can test the setup using any WebSocket client:

```javascript
// Browser console example
const ws = new WebSocket('ws://localhost:8085');
ws.onmessage = (event) => console.log('Received:', event.data);
ws.send('Hello from client!');
```

## Cleanup

Stop and remove all containers:
```bash
docker-compose down
```