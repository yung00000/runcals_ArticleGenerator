# Docker Troubleshooting Guide

## Issue: Container Restart Loop - Database Connection Errors

### Error: "Circuit breaker open: Too many authentication errors"

This error occurs when Supabase blocks connections after too many failed authentication attempts.

### Solutions

#### 1. Wait for Circuit Breaker to Reset

The circuit breaker typically resets after **5-10 minutes**. Wait before retrying.

#### 2. Verify .env File is Loaded in Docker

Check if environment variables are loaded correctly:

```bash
# Check if DATABASE_URL is set in container
docker exec runcals_article_generator_api env | grep DATABASE_URL

# Check all environment variables (masked)
docker exec runcals_article_generator_api env | grep -E "(DATABASE|API_KEY|SUPABASE)"
```

#### 3. Verify .env File Format

Ensure your `.env` file is in the project root and has correct format:

```env
# Database Connection (use Transaction Pooler URL for Docker)
DATABASE_URL=postgresql://postgres.dyvcdtsxrwyoevgsiuwf:YOUR_ENCODED_PASSWORD@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres

# Supabase
SUPABASE_URL=https://dyvcdtsxrwyoevgsiuwf.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Security
API_KEY=your-api-key
API_KEY_HEADER=X-API-Key
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Application
APP_NAME=runcals_ArticleGenerator
APP_VERSION=1.0.0
DEBUG=False
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

#### 4. Important: Use Connection Pooler URL

For Docker, **always use the Transaction Pooler URL** (port 6543):

1. Go to Supabase Dashboard → Settings → Database
2. Scroll to "Connection string"
3. Click "Connection pooling" tab
4. Select "Transaction" mode
5. Copy the URI

**Format:**
```
postgresql://postgres.dyvcdtsxrwyoevgsiuwf:PASSWORD@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
```

#### 5. URL-Encode Special Characters in Password

If your password contains special characters, encode them:

- `#` → `%23`
- `$` → `%24`
- `@` → `%40`
- `&` → `%26`
- `%` → `%25`

**Example:**
- Password: `mypass##123`
- Encoded: `mypass%23%23123`
- Full URL: `postgresql://postgres.dyvcdtsxrwyoevgsiuwf:mypass%23%23123@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres`

#### 6. Test Database Connection from Container

```bash
# Enter the container
docker exec -it runcals_article_generator_api bash

# Test Python import
python -c "from app.config import settings; print('DATABASE_URL set:', bool(settings.DATABASE_URL))"

# Test database connection
python -c "from app.database import db; import asyncio; asyncio.run(db.connect())"
```

#### 7. Rebuild Container After .env Changes

After updating `.env` file:

```bash
# Stop container
docker-compose down

# Rebuild and start
docker-compose up -d --build
```

#### 8. Check Container Logs

```bash
# View recent logs
docker logs --tail 100 runcals_article_generator_api

# Follow logs in real-time
docker logs -f runcals_article_generator_api
```

### Common Issues

#### Issue: .env file not found

**Solution:** Ensure `.env` file is in the same directory as `docker-compose.yml`

#### Issue: DATABASE_URL is empty in container

**Solution:** 
1. Check `.env` file exists and has `DATABASE_URL=...`
2. Verify no extra spaces around `=`
3. Rebuild container: `docker-compose up -d --build`

#### Issue: Password encoding errors

**Solution:** Use `python scripts/encode_password.py` to encode your password correctly

#### Issue: Wrong connection URL format

**Solution:** Use Transaction Pooler URL (port 6543) from Supabase Dashboard

### Prevention

1. **Always use Transaction Pooler URL** for Docker deployments
2. **URL-encode passwords** with special characters
3. **Test connection locally** before deploying to Docker
4. **Wait 5-10 minutes** if circuit breaker is open before retrying
5. **Check logs** immediately after starting container

### Still Having Issues?

1. Verify Supabase database is accessible from your network
2. Check Supabase Dashboard for any service issues
3. Verify your IP is not blocked by Supabase firewall
4. Try connecting from your local machine (outside Docker) to verify credentials

