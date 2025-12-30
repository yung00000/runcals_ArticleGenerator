# API Security Features

This API includes comprehensive security features to protect endpoints and control access from frontend applications.

## Security Features

### 1. API Key Authentication

All API endpoints (except health check and docs) require a valid API key in the request header.

**Header Format:**
```
X-API-Key: your-secret-api-key-here
```

**Excluded Endpoints:**
- `/` - Root endpoint
- `/docs` - Swagger UI documentation
- `/redoc` - ReDoc documentation
- `/openapi.json` - OpenAPI schema
- `/api/v1/health` - Health check endpoint

### 2. Rate Limiting

Rate limiting prevents API abuse by limiting the number of requests per IP address.

**Limits:**
- **Per Minute:** 60 requests
- **Per Hour:** 1000 requests

**Rate Limit Headers:**
- `X-RateLimit-Limit-Minute`: Maximum requests per minute
- `X-RateLimit-Remaining-Minute`: Remaining requests this minute
- `X-RateLimit-Limit-Hour`: Maximum requests per hour
- `X-RateLimit-Remaining-Hour`: Remaining requests this hour

**Rate Limit Response:**
When limit is exceeded, API returns `429 Too Many Requests` with `Retry-After` header.

### 3. Security Headers

All responses include security headers:

- `X-Content-Type-Options: nosniff` - Prevents MIME type sniffing
- `X-Frame-Options: DENY` - Prevents clickjacking attacks
- `X-XSS-Protection: 1; mode=block` - XSS protection
- `Strict-Transport-Security: max-age=31536000; includeSubDomains` - HTTPS enforcement
- `Referrer-Policy: strict-origin-when-cross-origin` - Controls referrer information

### 4. CORS Configuration

CORS is configured to allow only specified origins. Update `CORS_ORIGINS` in `.env` for your frontend domains.

## Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Security Settings
API_KEY=your-secret-api-key-here-change-in-production
API_KEY_HEADER=X-API-Key
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

### Generate Secure API Key

Generate a secure API key using Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Or use online tools to generate a strong random string.

## Frontend Integration

### JavaScript/TypeScript Example

```javascript
// Set API key in your frontend configuration
const API_KEY = 'your-secret-api-key-here';
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Make authenticated requests
async function fetchArticles() {
  const response = await fetch(`${API_BASE_URL}/articles`, {
    headers: {
      'X-API-Key': API_KEY,
      'Content-Type': 'application/json'
    }
  });
  
  if (!response.ok) {
    if (response.status === 401) {
      console.error('API key missing or invalid');
    } else if (response.status === 429) {
      console.error('Rate limit exceeded');
    }
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return await response.json();
}
```

### React Example

```typescript
// config.ts
export const API_CONFIG = {
  baseUrl: 'http://localhost:8000/api/v1',
  apiKey: process.env.REACT_APP_API_KEY || 'your-api-key'
};

// api.ts
export async function getArticles() {
  const response = await fetch(`${API_CONFIG.baseUrl}/articles`, {
    headers: {
      'X-API-Key': API_CONFIG.apiKey,
      'Content-Type': 'application/json'
    }
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return response.json();
}
```

### Axios Example

```javascript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'X-API-Key': 'your-secret-api-key-here',
    'Content-Type': 'application/json'
  }
});

// Use the client
const articles = await apiClient.get('/articles');
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "API key required. Please provide X-API-Key header."
}
```

### 403 Forbidden
```json
{
  "detail": "Invalid API key."
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded. Maximum 60 requests per minute."
}
```

## Best Practices

1. **Never commit API keys to version control**
   - Store API keys in environment variables
   - Use `.env` file (already in `.gitignore`)
   - Use different keys for development and production

2. **Rotate API keys regularly**
   - Change API keys periodically
   - Revoke compromised keys immediately

3. **Use HTTPS in production**
   - Never send API keys over HTTP
   - Configure SSL/TLS certificates

4. **Monitor rate limits**
   - Check rate limit headers in responses
   - Implement retry logic with exponential backoff

5. **Handle errors gracefully**
   - Check for 401/403 errors
   - Display user-friendly error messages
   - Log security events

## Testing

### Test API Key Authentication

```bash
# Without API key (should fail)
curl http://localhost:8000/api/v1/articles

# With API key (should succeed)
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/articles
```

### Test Rate Limiting

```bash
# Make multiple rapid requests
for i in {1..65}; do
  curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/articles
done
# 65th request should return 429
```

## Disabling Security (Development Only)

For development/testing, you can disable security features:

```env
# Disable API key requirement
API_KEY=

# Disable rate limiting
RATE_LIMIT_ENABLED=False
```

**⚠️ Warning:** Never disable security in production!

