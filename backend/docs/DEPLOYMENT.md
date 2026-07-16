# RAG-Sec Backend Deployment Guide

This guide covers deploying RAG-Sec backend to various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Health Checks](#health-checks)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 7.0+
- pip/venv

### Setup

1. **Clone repository and create virtual environment**

```bash
git clone <repository>
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment**

```bash
cp .env.example .env
# Edit .env with your local settings
```

4. **Initialize database**

```bash
# Start PostgreSQL
# Then run:
python -c "from database.init_db import init_db; init_db()"
```

5. **Run application**

```bash
python main.py
# Or with uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Application will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

---

## Docker Deployment

### Development with Docker Compose

**Start services:**

```bash
docker-compose up -d
```

This starts:
- PostgreSQL on port 5432
- Redis on port 6379
- RAG-Sec Backend on port 8000

**Check logs:**

```bash
docker-compose logs -f app
```

**Stop services:**

```bash
docker-compose down
```

**Remove volumes (reset data):**

```bash
docker-compose down -v
```

### Building Docker Image

**Build locally:**

```bash
docker build -t ragsec-backend:latest .
```

**Build multi-stage (optimized):**

```bash
docker build -t ragsec-backend:prod --target=runtime .
```

**Run container:**

```bash
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/db" \
  -e SECRET_KEY="your-secret-key" \
  ragsec-backend:latest
```

---

## Production Deployment

### Using docker-compose.prod.yml

1. **Configure environment file**

```bash
cp .env.example .env.prod
# Edit with production values:
export $(cat .env.prod | xargs)
```

2. **Set required secrets**

```bash
export DB_NAME="ragsec_prod"
export DB_USER="postgres"
export DB_PASSWORD="$(openssl rand -base64 32)"
export SECRET_KEY="$(openssl rand -base64 48)"
export REDIS_PASSWORD="$(openssl rand -base64 32)"
```

3. **Start production stack**

```bash
docker-compose -f docker-compose.prod.yml up -d
```

4. **Verify deployment**

```bash
curl http://localhost:8000/health
```

### SSL/TLS Configuration

1. **Generate self-signed certificates (testing only)**

```bash
mkdir -p certs
openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes
```

2. **Use Let's Encrypt in production**

```bash
# Via Nginx:
certbot certonly --webroot -w /var/www/certbot -d yourdomain.com
```

### Production Checklist

- [ ] Change all default passwords
- [ ] Set `DEBUG=false`
- [ ] Update `SECRET_KEY` with strong value
- [ ] Configure `CORS_ORIGINS` for your domain
- [ ] Set up SSL/TLS certificates
- [ ] Enable database backups
- [ ] Configure logging and monitoring
- [ ] Set up health checks
- [ ] Test disaster recovery procedures
- [ ] Review security settings
- [ ] Set resource limits

---

## Kubernetes Deployment

### Prerequisites

- kubectl installed and configured
- Kubernetes cluster (1.24+)
- Helm (optional, for package management)

### Create Kubernetes Manifests

**Create namespace:**

```bash
kubectl create namespace ragsec-prod
```

**Create secrets:**

```bash
kubectl create secret generic ragsec-secrets \
  --from-literal=db-password="$(openssl rand -base64 32)" \
  --from-literal=secret-key="$(openssl rand -base64 48)" \
  --from-literal=redis-password="$(openssl rand -base64 32)" \
  -n ragsec-prod
```

**Create ConfigMap:**

```bash
kubectl create configmap ragsec-config \
  --from-file=app/config/settings.py \
  -n ragsec-prod
```

**Deploy using manifests:**

```bash
# See k8s/ directory for manifest files
kubectl apply -f k8s/ -n ragsec-prod
```

**Check deployment status:**

```bash
kubectl get pods -n ragsec-prod
kubectl get services -n ragsec-prod
```

**View logs:**

```bash
kubectl logs -f deployment/ragsec-backend -n ragsec-prod
```

---

## Environment Configuration

### Required Environment Variables

```bash
# Application
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ragsec_db
DB_USER=postgres
DB_PASSWORD=secure_password

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=secure_password

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=["https://yourdomain.com"]
```

### Optional Environment Variables

```bash
# HSM
ENABLE_HSM_SIMULATION=false
HSM_KEY_ROTATION_MINUTES=5

# Features
ENABLE_HONEY_TABLE_DETECTION=true
ENABLE_DECEPTION_ROUTING=true
ENABLE_REQUEST_LOGGING=true

# Database Connection Pool
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
```

---

## Health Checks

### Application Health Endpoint

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "RAG-Sec Backend",
  "database": "connected",
  "hsm_key_id": "key_2024_001",
  "hsm_key_age_minutes": 2.5
}
```

### Docker Health Check

```bash
docker inspect --format='{{.State.Health.Status}}' <container_id>
```

### Kubernetes Health Checks

Configured in deployment manifests:
- Liveness probe: Checks if pod is running
- Readiness probe: Checks if pod is ready to accept traffic
- Startup probe: Checks if pod has started

---

## Monitoring

### Prometheus Metrics

Metrics endpoint: `/metrics`

```bash
curl http://localhost:8000/metrics
```

### Application Logs

**Local:**
```bash
tail -f app.log
```

**Docker:**
```bash
docker logs -f <container_id>
```

**Kubernetes:**
```bash
kubectl logs -f pod/<pod_name> -n ragsec-prod
```

### Performance Monitoring

Monitor these metrics:
- Response time (p50, p95, p99)
- Request rate (requests/second)
- Error rate (errors/minute)
- Database connection pool usage
- Memory usage
- CPU usage

---

## Troubleshooting

### Application won't start

1. Check environment variables
```bash
env | grep DATABASE_URL
```

2. Verify database connectivity
```bash
psql $DATABASE_URL -c "SELECT 1;"
```

3. Check logs
```bash
docker logs <container_id>
```

### Database connection timeout

```bash
# Test connection
nc -zv db_host 5432

# Check connection pool
curl http://localhost:8000/health
```

### High memory usage

1. Check for memory leaks
```bash
docker stats <container_id>
```

2. Restart container
```bash
docker restart <container_id>
```

3. Reduce connection pool size in .env

### Slow queries

1. Enable query logging in PostgreSQL
2. Identify slow queries
3. Add appropriate indexes
4. Consider query optimization

### Rate limiting issues

Check middleware configuration in `main.py`

### Authentication failures

1. Verify JWT_SECRET_KEY is consistent
2. Check token expiration
3. Review logs for auth errors

---

## Backup & Recovery

### Database Backup

```bash
# Backup
pg_dump -U postgres ragsec_db > backup.sql

# Restore
psql -U postgres ragsec_db < backup.sql
```

### Automated Backups

See `docs/BACKUP_RECOVERY.md` for detailed procedures.

---

## Performance Tuning

### Database

- Configure PostgreSQL connection pool
- Enable query caching with Redis
- Add appropriate indexes
- Monitor slow queries

### Application

- Use horizontal scaling (multiple replicas)
- Configure load balancer
- Enable compression
- Use CDN for static assets

### Deployment

- Use container orchestration
- Implement auto-scaling
- Monitor resource usage
- Set appropriate resource limits

---

## Support

For issues or questions:

1. Check logs and health endpoint
2. Review troubleshooting section
3. Consult documentation
4. Contact support team

---

**Last Updated:** July 16, 2026  
**Maintained By:** RAG-Sec Team
