# SQLAlchemy with Session Pooler Setup

This project now uses **SQLAlchemy** with **Session Pooler** connection method as recommended by Supabase for persistent backend applications.

## Connection Method

We're using **Session Pooler** which:
- ✅ Supports both IPv4 and IPv6
- ✅ Ideal for persistent backend services (like FastAPI)
- ✅ Uses port 5432
- ✅ Better reliability than direct connection

## Dependencies

The following packages are required:
- `sqlalchemy==2.0.23` - SQLAlchemy ORM
- `psycopg2-binary==2.9.9` - PostgreSQL adapter for Python

## Connection String Format

Your `.env` file should use the `DATABASE_URL` format matching pgAdmin 4 settings:

**Transaction Mode Pooler (Recommended - matches pgAdmin 4):**
```env
DATABASE_URL=postgresql://postgres.dyvcdtsxrwyoevgsiuwf:password@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres
```

**Or use individual parameters (matches pgAdmin 4 exactly):**
```env
user=postgres.dyvcdtsxrwyoevgsiuwf
password=your_password
host=aws-1-ap-southeast-1.pooler.supabase.com
port=6543
dbname=postgres
```

**Important:**
- Username format: `postgres.dyvcdtsxrwyoevgsiuwf` (project-specific)
- Host: `aws-1-ap-southeast-1.pooler.supabase.com` (shared pooler)
- Port: `6543` (Transaction mode)
- URL-encode special characters in password when using DATABASE_URL (`##` becomes `%23%23`)
- Individual parameters handle encoding automatically

## How It Works

1. **SQLAlchemy Async Engine**: Creates an async connection engine
2. **Connection Pooling**: Automatically manages connection pool (size: 5, max overflow: 10)
3. **Session Management**: Uses async sessions for database operations
4. **Parameter Binding**: Uses named parameters (`:param_name`) instead of positional (`$1`)

## Code Changes

### Database Layer (`app/database.py`)
- Uses `create_async_engine` from SQLAlchemy
- Creates async session maker
- Methods use named parameters (`**kwargs`)

### Service Layer (`app/services/article_service.py`)
- Updated all queries to use named parameters (`:param_name`)
- Changed from `$1, $2` to `:param_name` format

## Getting Your Connection String

1. Go to Supabase Dashboard → Settings → Database
2. Click "Connection pooling" tab
3. Select "Session pooler" (for persistent backends)
4. Copy the connection string
5. Update `DATABASE_URL` in `.env`

## Testing

After updating your `.env` file:

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload
```

The server will automatically:
- Connect using SQLAlchemy
- Use connection pooling
- Handle async operations properly

