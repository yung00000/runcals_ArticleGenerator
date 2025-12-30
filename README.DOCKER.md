# Docker Deployment Guide

This guide explains how to build and run the runcals_ArticleGenerator API using Docker Desktop on Windows.

## Prerequisites

1. **Docker Desktop** installed and running on Windows
2. **.env file** configured with all required environment variables
3. **Network access** to your Supabase database

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Build and start the container:**
   ```bash
   docker-compose up -d --build
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Stop the container:**
   ```bash
   docker-compose down
   ```

4. **Restart the container:**
   ```bash
   docker-compose restart
   ```

### Option 2: Using Docker Commands

1. **Build the image:**
   ```bash
   docker build -t runcals-article-generator:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name runcals-api \
     -p 8000:8000 \
     --env-file .env \
     --restart unless-stopped \
     runcals-article-generator:latest
   ```

3. **View logs:**
   ```bash
   docker logs -f runcals-api
   ```

4. **Stop the container:**
   ```bash
   docker stop runcals-api
   docker rm runcals-api
   ```

## Environment Variables

Make sure your `.env` file contains all required variables:

```env
# Supabase Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Database Connection
DATABASE_URL=postgresql://user:password@host:port/dbname

# Security
API_KEY=your-api-key-here
API_KEY_HEADER=X-API-Key
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Application Settings
APP_NAME=runcals_ArticleGenerator
APP_VERSION=1.0.0
DEBUG=False
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Accessing the API

Once the container is running:

- **API Base URL:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/api/v1/health

## Docker Commands Reference

### View Running Containers
```bash
docker ps
```

### View All Containers (including stopped)
```bash
docker ps -a
```

### View Container Logs
```bash
docker logs runcals-api
docker logs -f runcals-api  # Follow logs
```

### Execute Commands in Container
```bash
docker exec -it runcals-api bash
docker exec -it runcals-api python -c "from app.config import settings; print(settings.API_KEY)"
```

### View Container Resource Usage
```bash
docker stats runcals-api
```

### Rebuild After Code Changes
```bash
docker-compose up -d --build
# Or with Docker:
docker build -t runcals-article-generator:latest .
docker stop runcals-api && docker rm runcals-api
docker run -d --name runcals-api -p 8000:8000 --env-file .env runcals-article-generator:latest
```

## Troubleshooting

### Container Won't Start

1. **Check logs:**
   ```bash
   docker logs runcals-api
   ```

2. **Verify .env file exists and is correct:**
   ```bash
   # On Windows PowerShell
   Get-Content .env
   ```

3. **Check if port 8000 is already in use:**
   ```bash
   netstat -ano | findstr :8000
   ```

### Database Connection Issues

1. **Verify DATABASE_URL in .env:**
   - Ensure password is URL-encoded (special characters like `#` should be `%23`)
   - Use Transaction Pooler URL (port 6543) for better compatibility

2. **Test connection from container:**
   ```bash
   docker exec -it runcals-api python -c "from app.database import db; import asyncio; asyncio.run(db.connect())"
   ```

### API Key Not Working

1. **Verify API_KEY is set in .env:**
   ```bash
   docker exec -it runcals-api python -c "from app.config import settings; print('API_KEY set:', bool(settings.API_KEY))"
   ```

2. **Check middleware logs:**
   ```bash
   docker logs runcals-api | grep APIKeyMiddleware
   ```

## Production Deployment

For production deployment:

1. **Set DEBUG=False** in `.env`
2. **Use strong API_KEY** (generate with `python scripts/generate_api_key.py`)
3. **Configure proper CORS_ORIGINS** for your frontend domain
4. **Use HTTPS** (configure reverse proxy like Nginx)
5. **Set up proper logging** and monitoring
6. **Use Docker secrets** or environment variables instead of .env file in production

## Multi-Stage Build Benefits

The production Dockerfile uses a multi-stage build:

- **Stage 1 (builder):** Installs build dependencies and compiles Python packages
- **Stage 2 (runtime):** Only includes runtime dependencies, resulting in a smaller image

This reduces the final image size and improves security by excluding build tools.

## Health Check

The container includes a health check that monitors the `/api/v1/health` endpoint:

- **Interval:** Every 30 seconds
- **Timeout:** 10 seconds
- **Retries:** 3 attempts
- **Start Period:** 40 seconds (allows time for startup)

Check health status:
```bash
docker inspect --format='{{.State.Health.Status}}' runcals-api
```

## Security Notes

1. **Non-root user:** Container runs as `appuser` (UID 1000) for security
2. **No build tools:** Production image excludes gcc and build dependencies
3. **Minimal base image:** Uses `python:3.11-slim` for smaller attack surface
4. **Environment variables:** Sensitive data passed via .env file, not baked into image

## Windows-Specific Notes

1. **Line endings:** Docker handles Windows line endings automatically
2. **Path separators:** Use forward slashes in Dockerfile (Docker handles conversion)
3. **Volume mounts:** Use Windows-style paths when mounting volumes
4. **File permissions:** Docker Desktop handles file permissions automatically

## Next Steps

- Set up reverse proxy (Nginx/Traefik) for HTTPS
- Configure Docker Swarm or Kubernetes for orchestration
- Set up CI/CD pipeline for automated deployments
- Configure monitoring and logging (Prometheus, Grafana, ELK stack)

