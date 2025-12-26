# 🐳 Docker Setup Guide

## Quick Start with Docker

### Prerequisites
- Docker installed (https://www.docker.com/get-started)
- Docker Compose installed
- `.env` file configured

---

## 🚀 Build and Run

### Option 1: Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

### Option 2: Docker Only

```bash
# Build image
docker build -t spectrum-bridge-ai .

# Run container
docker run -d \
  --name spectrum-bridge-ai \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/knowledge_base:/app/knowledge_base \
  -v $(pwd)/output:/app/output \
  spectrum-bridge-ai

# View logs
docker logs -f spectrum-bridge-ai

# Stop container
docker stop spectrum-bridge-ai
docker rm spectrum-bridge-ai
```

---

## 📦 What's Included

The Docker container includes:
- ✅ Python 3.12-slim base
- ✅ All dependencies installed
- ✅ Non-root user for security
- ✅ Health checks configured
- ✅ Volume mounts for data persistence

---

## 🔧 Configuration

### Environment Variables

The container uses `.env` file for configuration:

```bash
# Required
MONGODB_URI=your_mongodb_uri
GROQ_API_KEY=your_groq_key

# Optional
HF_TOKEN=your_hf_token
```

### Volumes

```yaml
volumes:
  - ./knowledge_base:/app/knowledge_base  # PDFs and embeddings
  - ./output:/app/output                  # Generated files
```

This ensures:
- PDFs persist across container restarts
- Generated images are accessible
- Embeddings are reused

---

## 🧪 Testing Docker Setup

### Test 1: Build Success

```bash
docker build -t spectrum-bridge-ai .
```

Expected: Build completes without errors

### Test 2: Container Starts

```bash
docker-compose up -d
docker-compose ps
```

Expected: Container status shows "Up"

### Test 3: Health Check

```bash
docker-compose exec spectrum-bridge-ai python -c "print('✓ Container healthy')"
```

Expected: Prints success message

### Test 4: Run Agent

```bash
docker-compose exec spectrum-bridge-ai python -c "
from agents.content_adapter import ContentAdapter
adapter = ContentAdapter()
result = adapter.simplify_text('Test text')
print('✓ Agents working' if result['success'] else '✗ Failed')
"
```

Expected: "✓ Agents working"

---

## 🐛 Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker-compose logs
```

**Common issues:**
- Missing .env file → Create from .env.example
- Port 8000 in use → Change port in docker-compose.yml
- Permission issues → Check file ownership

### Can't Access MongoDB

**Test connection:**
```bash
docker-compose exec spectrum-bridge-ai python -c "
from pymongo import MongoClient
import os
client = MongoClient(os.getenv('MONGODB_URI'))
print(client.server_info())
"
```

**Fix:**
- Check MONGODB_URI in .env
- Verify network access in MongoDB Atlas
- Check firewall rules

### Dependencies Missing

**Rebuild without cache:**
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 Container Resources

### Minimum Requirements
- **CPU:** 2 cores
- **RAM:** 4GB
- **Disk:** 10GB

### Recommended
- **CPU:** 4 cores (for faster image generation)
- **RAM:** 8GB
- **Disk:** 20GB

### Resource Limits

Edit `docker-compose.yml`:

```yaml
services:
  spectrum-bridge-ai:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          memory: 2G
```

---

## 🔒 Security

### Best Practices

1. **Don't include .env in image**
   - Use `--env-file` or environment variables
   - Never commit .env to Git

2. **Run as non-root**
   - Already configured in Dockerfile
   - User: appuser (UID 1000)

3. **Keep images updated**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

4. **Scan for vulnerabilities**
   ```bash
   docker scan spectrum-bridge-ai
   ```

---

## 📦 Multi-Stage Builds (Advanced)

For smaller images, use multi-stage build:

```dockerfile
# Builder stage
FROM python:3.12 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.12-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
CMD ["python", "api/main.py"]
```

---

## 🌐 Production Deployment

### Using Docker on Cloud Platforms

#### AWS ECS
```bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin
docker tag spectrum-bridge-ai:latest xxx.ecr.region.amazonaws.com/spectrum-bridge-ai
docker push xxx.ecr.region.amazonaws.com/spectrum-bridge-ai
```

#### Google Cloud Run
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/spectrum-bridge-ai

# Deploy
gcloud run deploy spectrum-bridge-ai \
  --image gcr.io/PROJECT_ID/spectrum-bridge-ai \
  --platform managed
```

#### Azure Container Instances
```bash
# Create container
az container create \
  --resource-group myResourceGroup \
  --name spectrum-bridge-ai \
  --image spectrum-bridge-ai:latest \
  --dns-name-label spectrum-bridge
```

---

## ✅ Docker Checklist

- [ ] Dockerfile created and tested
- [ ] docker-compose.yml configured
- [ ] .env.example provided
- [ ] .dockerignore created
- [ ] Health checks working
- [ ] Volumes properly mounted
- [ ] Non-root user configured
- [ ] Build succeeds
- [ ] Container runs successfully
- [ ] Agents work inside container
- [ ] Documentation complete

---

## 🎯 Next Steps

1. ✅ Build Docker image
2. ✅ Test locally with docker-compose
3. ✅ Push to Docker Hub (optional)
4. ✅ Deploy to cloud (optional)
5. ✅ Set up CI/CD (optional)

---

**Docker setup complete! Your application is containerized and ready for deployment anywhere.** 🐳
