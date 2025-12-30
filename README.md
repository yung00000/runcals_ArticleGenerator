# runcals_ArticleGenerator

Backend API for Article Generator built with FastAPI and Supabase PostgreSQL.

## Features

- 🚀 FastAPI with async/await support
- 🗄️ Supabase PostgreSQL database integration
- 🔌 **MCP (Model Context Protocol) integration** for database management
- 🔒 Environment-based configuration with `.env` file
- 📝 API versioning (v1)
- 🛡️ **Security Features:**
  - 🔑 API Key authentication
  - ⏱️ Rate limiting (60/min, 1000/hour)
  - 🔐 Security headers (XSS, clickjacking protection)
  - 🌐 CORS middleware for frontend integration
- 📊 Request logging and error handling
- 🏥 Health check endpoint
- 📚 Auto-generated API documentation

## Project Structure

```
runcals_ArticleGenerator/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration & environment variables
│   ├── database.py             # Supabase PostgreSQL connection
│   ├── dependencies.py         # Shared dependencies
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── router.py       # API router aggregation
│   │       └── endpoints/
│   │           ├── health.py   # Health check endpoint
│   │           └── articles.py # Article CRUD endpoints
│   │
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   │
│   ├── services/
│   │   └── article_service.py  # Business logic layer
│   │
│   ├── middleware/
│   │   ├── cors.py             # CORS configuration
│   │   ├── logging.py          # Request logging
│   │   └── error_handler.py    # Global error handling
│   │
│   └── utils/
│       └── logger.py           # Logging configuration
│
├── .env                        # Environment variables (create from .env.example)
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt            # Python dependencies
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory based on `.env.example`:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your Supabase credentials:

**Option 1: Using DATABASE_URL (Recommended)**
```env
# Supabase Configuration
SUPABASE_URL=https://dyvcdtsxrwyoevgsiuwf.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Database Connection - Transaction Pooler (matches pgAdmin 4 settings)
DATABASE_URL=postgresql://postgres.dyvcdtsxrwyoevgsiuwf:your_password@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres
```

**Option 2: Using Individual Parameters (matches pgAdmin 4 exactly)**
```env
# Supabase Configuration
SUPABASE_URL=https://dyvcdtsxrwyoevgsiuwf.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Database Connection - Individual parameters (same as pgAdmin 4)
user=postgres.dyvcdtsxrwyoevgsiuwf
password=your_password
host=aws-1-ap-southeast-1.pooler.supabase.com
port=6543
dbname=postgres
```

**Important Notes:**
- **Transaction Pooler** (port 6543): Works with pgAdmin 4 and FastAPI
- Username format: `postgres.dyvcdtsxrwyoevgsiuwf` (project-specific)
- Host: `aws-1-ap-southeast-1.pooler.supabase.com` (shared pooler)
- URL-encode special characters in password when using DATABASE_URL (`##` → `%23%23`)
- Individual parameters handle encoding automatically

### 3. Get Supabase Credentials

**Option A: Using MCP (Recommended - Already Connected!)**

Your Supabase project is already connected via MCP:
- **Project URL**: `https://dyvcdtsxrwyoevgsiuwf.supabase.co`
- **Project Ref**: `dyvcdtsxrwyoevgsiuwf`
- **API Key**: Already available via MCP

You only need to get your database password:
1. Go to Supabase Dashboard → **Settings** → **Database**
2. Copy the **Connection string** → `DATABASE_URL`
   - Format: `postgresql://postgres:[YOUR-PASSWORD]@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres`

**Option B: Manual Setup**

1. Go to your Supabase project dashboard
2. Navigate to **Settings** → **API**
3. Copy the following:
   - **Project URL** → `SUPABASE_URL`
   - **anon public** key → `SUPABASE_KEY`
   - **service_role** key → `SUPABASE_SERVICE_ROLE_KEY`
4. Navigate to **Settings** → **Database**
5. Copy the **Connection string** → `DATABASE_URL`

### 4. Database Schema

✅ **Already Configured!** The `running_articles` table exists in your database:
- `id` (bigint, primary key)
- `created_at` (timestamptz)
- `title` (varchar, nullable)
- `content` (text, nullable)

⚠️ **Important: RLS Policies Required**

The table has Row Level Security (RLS) enabled but needs policies. Run this SQL via MCP or Supabase Dashboard:

```sql
-- See scripts/create_rls_policies.sql for full policies
CREATE POLICY "Allow public read access" ON running_articles FOR SELECT USING (true);
CREATE POLICY "Allow public insert" ON running_articles FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public update" ON running_articles FOR UPDATE USING (true);
CREATE POLICY "Allow public delete" ON running_articles FOR DELETE USING (true);
```

Or use the service role key in your backend for server-side operations (more secure).

### 5. Run the Application

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python -m app.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check API and database status

### Articles
- `GET /api/v1/articles` - Get all articles (with pagination and date filtering)
- `GET /api/v1/articles/{id}` - Get article by ID
- `POST /api/v1/articles` - Create new article
- `PUT /api/v1/articles/{id}` - Update article
- `DELETE /api/v1/articles/{id}` - Delete article

### Query Parameters for Articles List
- `page` (default: 1) - Page number
- `page_size` (default: 10, max: 100) - Items per page
- `date_from` (optional) - Filter articles from this date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
- `date_to` (optional) - Filter articles until this date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)

## Example API Requests

### Get All Articles
```bash
curl http://localhost:8000/api/v1/articles?page=1&page_size=10
```

### Get Articles by Date Range
```bash
# Get articles from December 20, 2025
curl "http://localhost:8000/api/v1/articles?date_from=2025-12-20"

# Get articles between December 20-28, 2025
curl "http://localhost:8000/api/v1/articles?date_from=2025-12-20&date_to=2025-12-28"

# Get articles on specific date
curl "http://localhost:8000/api/v1/articles?date_from=2025-12-28&date_to=2025-12-28"

# With pagination
curl "http://localhost:8000/api/v1/articles?date_from=2025-12-20&page=1&page_size=20"
```

### Create Article
```bash
curl -X POST http://localhost:8000/api/v1/articles \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Article",
    "content": "This is the content",
    "author": "John Doe"
  }'
```

### Get Article by ID
```bash
curl http://localhost:8000/api/v1/articles/1
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_KEY` | Supabase anon/public key | Yes |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key | No |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `APP_NAME` | Application name | No |
| `APP_VERSION` | Application version | No |
| `DEBUG` | Enable debug mode | No |
| `ENVIRONMENT` | Environment (development/production) | No |
| `HOST` | Server host | No |
| `PORT` | Server port | No |
| `CORS_ORIGINS` | Comma-separated list of allowed origins | No |

## Development

### Project Structure Principles

- **Separation of Concerns**: Routes → Services → Database
- **API Versioning**: All endpoints under `/api/v1/`
- **Error Handling**: Centralized error handling middleware
- **Logging**: Structured logging for all requests
- **Type Safety**: Pydantic models for request/response validation

### Adding New Endpoints

1. Create service in `app/services/`
2. Create schema in `app/models/schemas.py`
3. Create endpoint in `app/api/v1/endpoints/`
4. Register router in `app/api/v1/router.py`

## Deployment

### Serverless Deployment (AWS Lambda, Vercel, etc.)

The application is structured to be serverless-ready. For deployment:

1. Ensure environment variables are set in your deployment platform
2. Use a serverless adapter like `mangum` for AWS Lambda:
   ```bash
   pip install mangum
   ```
3. Update deployment configuration as needed

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## MCP Integration

This project uses **MCP (Model Context Protocol)** for Supabase database management. You can:

- Query database directly via MCP tools
- Apply migrations using `mcp_supabase_apply_migration`
- Check logs using `mcp_supabase_get_logs`
- Generate TypeScript types using `mcp_supabase_generate_typescript_types`

See [docs/MCP_SUPABASE_GUIDE.md](docs/MCP_SUPABASE_GUIDE.md) for detailed MCP usage.

## Security Features

### API Key Authentication

All API endpoints require a valid API key in the `X-API-Key` header (except health check and docs).

**Generate API Key:**
```bash
python scripts/generate_api_key.py
```

**Add to .env:**
```env
API_KEY=your-generated-api-key-here
```

**Frontend Usage:**
```javascript
fetch('/api/v1/articles', {
  headers: {
    'X-API-Key': 'your-api-key-here'
  }
})
```

### Rate Limiting

- **60 requests per minute** per IP address
- **1000 requests per hour** per IP address
- Rate limit headers included in responses

### Security Headers

All responses include security headers:
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Strict-Transport-Security
- Referrer-Policy

See [docs/SECURITY.md](docs/SECURITY.md) for detailed security documentation.

## Security Notes

- ⚠️ Never commit `.env` file to version control
- 🔒 Use environment variables for all sensitive data
- 🔑 Generate strong API keys and rotate them regularly
- 🛡️ Configure CORS origins properly for production
- 🔐 **Create RLS policies** for `running_articles` table (see scripts/create_rls_policies.sql)
- 📝 Validate all inputs using Pydantic models
- ⏱️ Monitor rate limit headers in responses

## License

MIT
