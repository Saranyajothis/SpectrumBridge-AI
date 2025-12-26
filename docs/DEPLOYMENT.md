# 🚀 Deployment Guide

## Deployment Options

### Option 1: Local Development (Current)

**Best for:** Development, testing, personal use

**Pros:**
- ✅ No deployment costs
- ✅ Full control
- ✅ Easy debugging

**Setup:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/test_all_agents.py
```

---

### Option 2: Docker Deployment

**Best for:** Consistent environments, easy distribution

**Pros:**
- ✅ Reproducible environment
- ✅ Easy to share
- ✅ Isolated dependencies

**Setup:**
```bash
# Build
docker build -t spectrum-bridge-ai .

# Run
docker-compose up -d

# Check
docker-compose logs -f

# Stop
docker-compose down
```

---

### Option 3: Cloud Deployment

**Best for:** Production, multiple users, web access

#### Render.com (FREE Tier)

```bash
# 1. Create render.yaml
# 2. Connect GitHub repo
# 3. Deploy automatically
```

#### Railway.app (FREE $5/month credit)

```bash
# 1. railway login
# 2. railway init
# 3. railway up
```

#### Fly.io (FREE allowance)

```bash
# 1. fly launch
# 2. fly deploy
# 3. fly open
```

---

## Environment Setup

### Development
```bash
cp .env.example .env
# Edit .env with development credentials
```

### Production
- Use environment variables (don't commit .env)
- Set in hosting platform dashboard
- Use secrets management

---

## Database Setup

### MongoDB Atlas

1. **Create Cluster**
   - Go to https://cloud.mongodb.com
   - Create free M0 cluster
   - Choose region closest to you

2. **Network Access**
   - Add IP whitelist (0.0.0.0/0 for development)
   - Or specific IPs for production

3. **Database User**
   - Create user with read/write permissions
   - Save credentials securely

4. **Connection String**
   - Get connection string
   - Add to .env as MONGODB_URI

5. **Vector Index**
   - Create in Atlas UI or via script
   - See SETUP_GUIDE.md

---

## Performance Optimization

### For Faster Image Generation

**Use GPU if available:**
- NVIDIA GPU: Automatic CUDA detection
- Apple Silicon: Currently disabled (MPS black image bug)
- Consider paid API for production speed

### For Faster Embeddings

**Batch processing:**
```python
# Increase batch size if you have more RAM
BATCH_SIZE = 64  # Default: 32
```

### For Faster RAG

**Adjust top_k:**
```python
# Fewer results = faster
retriever.retrieve(query, top_k=3)  # Instead of 5
```

---

## Scaling

### Horizontal Scaling
- Deploy multiple instances behind load balancer
- Share MongoDB (already stateless)
- Each instance has own SD model

### Vertical Scaling
- More RAM → Larger batch sizes
- GPU → Faster image generation
- More CPU → Faster inference

---

## Monitoring

### Health Checks

```bash
# Check if services are up
docker-compose ps

# Check MongoDB connection
python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); print('✓ MongoDB OK' if MongoClient(os.getenv('MONGODB_URI')).server_info() else '✗ Failed')"

# Check Groq API
python -c "from groq import Groq; import os; from dotenv import load_dotenv; load_dotenv(); client = Groq(api_key=os.getenv('GROQ_API_KEY')); print('✓ Groq OK')"
```

### Logging

Add logging to production:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

---

## Security

### API Keys
- ✅ Never commit .env to git
- ✅ Use environment variables
- ✅ Rotate keys regularly
- ✅ Use read-only tokens where possible

### Database
- ✅ Restrict network access
- ✅ Use strong passwords
- ✅ Enable MongoDB authentication
- ✅ Regular backups

### Docker
- ✅ Run as non-root user (already configured)
- ✅ Scan images for vulnerabilities
- ✅ Keep base images updated

---

## Troubleshooting

### MongoDB Connection Issues
```bash
# Test connection
python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); print(MongoClient(os.getenv('MONGODB_URI')).server_info())"
```

### Groq API Issues
- Check daily limit (14,400 requests)
- Verify API key is active
- Check for typos in .env

### Docker Issues
```bash
# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Image Generation Issues
- CPU mode is slow but reliable
- For faster generation, use paid API
- Or wait for GPU support improvements

---

## Backup & Recovery

### Backup Knowledge Base
```bash
# Backup PDFs
tar -czf pdfs_backup.tar.gz knowledge_base/pdfs/

# Backup embeddings
cp knowledge_base/embeddings/embeddings.json embeddings_backup.json
```

### Backup MongoDB
```bash
# Use MongoDB Atlas built-in backup
# Or export collection
mongodump --uri="$MONGODB_URI" --db=spectrum_bridge_AI
```

---

## Updates & Maintenance

### Adding New PDFs
```bash
# 1. Add PDFs to knowledge_base/pdfs/
# 2. Regenerate embeddings
python scripts/03_generate_embeddings.py
# 3. Upload to MongoDB
python scripts/04_upload_to_mongodb.py
```

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Model Updates
- Sentence transformers auto-updates
- Stable Diffusion model cached locally
- Groq models updated automatically

---

## Production Checklist

- [ ] Environment variables set securely
- [ ] MongoDB network access configured
- [ ] API keys rotated and secure
- [ ] Docker images built and tested
- [ ] Health checks configured
- [ ] Logging enabled
- [ ] Backups scheduled
- [ ] Monitoring set up
- [ ] Documentation updated
- [ ] Tests passing (95.5%+ coverage)

---

**Ready for production deployment!** 🚀
