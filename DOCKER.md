# SuperMock Docker

## Quick Start with Docker

### Build the image:

```bash
docker build -t supermock:latest .
```

### Run the container:

```bash
docker run -d -p 8081:8081 --name supermock supermock:latest
```

### Or use Docker Compose:

```bash
docker-compose up -d
```

## Usage

Once running, your bot can connect to `http://localhost:8081/bot<YOUR_TOKEN>`

## Configuration

### Environment Variables:

- `SUPERMOCK_HOST`: Host to bind (default: 0.0.0.0)
- `SUPERMOCK_PORT`: Port to bind (default: 8081)

### Custom Configuration File:

Mount a config file to `/app/supermock.config.yaml`:

```bash
docker run -d \
  -p 8081:8081 \
  -v $(pwd)/supermock.config.yaml:/app/supermock.config.yaml \
  --name supermock \
  supermock:latest
```

## Persistent History

Mount a volume for persistent data:

```bash
docker run -d \
  -p 8081:8081 \
  -v supermock-data:/app/data \
  --name supermock \
  supermock:latest
```

## Health Check

Check if the server is running:

```bash
curl http://localhost:8081/bottest/getMe
```

## Stopping

```bash
docker stop supermock
docker rm supermock
```

Or with Docker Compose:

```bash
docker-compose down
```
