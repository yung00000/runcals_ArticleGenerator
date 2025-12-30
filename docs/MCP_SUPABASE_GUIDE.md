# Using Supabase MCP (Model Context Protocol)

This guide explains how to use MCP tools to manage your Supabase database directly from Cursor.

## MCP Connection Status

✅ **Connected Successfully**

- **Project URL**: `https://dyvcdtsxrwyoevgsiuwf.supabase.co`
- **Project Reference**: `dyvcdtsxrwyoevgsiuwf`

## Available MCP Tools

You can use these MCP tools in Cursor to interact with your Supabase database:

### Database Operations
- `mcp_supabase_execute_sql` - Execute raw SQL queries
- `mcp_supabase_list_tables` - List all tables in your database
- `mcp_supabase_apply_migration` - Apply database migrations
- `mcp_supabase_list_migrations` - List all migrations

### Project Information
- `mcp_supabase_get_project_url` - Get project URL
- `mcp_supabase_get_publishable_keys` - Get API keys
- `mcp_supabase_list_tables` - List database tables
- `mcp_supabase_list_extensions` - List PostgreSQL extensions

### Monitoring & Debugging
- `mcp_supabase_get_logs` - Get service logs
- `mcp_supabase_get_advisors` - Get security/performance recommendations

### Type Generation
- `mcp_supabase_generate_typescript_types` - Generate TypeScript types from schema

## Current Database Schema

### Tables Found:
1. **running_articles** (18 rows)
   - `id` (bigint, primary key)
   - `created_at` (timestamptz)
   - `title` (varchar, nullable)
   - `content` (text, nullable)

2. **runcal_article** (18 rows)
3. **membership** (0 rows)
4. **runinfo** (0 rows)
5. **users** (0 rows)
6. **n8n_chat_histories** (0 rows)

## Security Advisors

⚠️ **Important Security Notes:**

1. **RLS Policies Missing**: The `running_articles` table has Row Level Security (RLS) enabled but no policies exist. This means:
   - RLS is blocking all access by default
   - You need to create policies to allow API access

### Fix RLS Policies

Run this SQL via MCP or Supabase Dashboard:

```sql
-- Allow public read access (adjust based on your needs)
CREATE POLICY "Allow public read access" ON running_articles
FOR SELECT USING (true);

-- Allow public insert (adjust based on your needs)
CREATE POLICY "Allow public insert" ON running_articles
FOR INSERT WITH CHECK (true);

-- Allow public update (adjust based on your needs)
CREATE POLICY "Allow public update" ON running_articles
FOR UPDATE USING (true);

-- Allow public delete (adjust based on your needs)
CREATE POLICY "Allow public delete" ON running_articles
FOR DELETE USING (true);
```

Or use service role key in your backend (more secure for server-side operations).

## Example MCP Usage

### Query Data
```python
# In Cursor, you can ask:
# "Use MCP to query running_articles table"
# The AI will use: mcp_supabase_execute_sql
```

### Apply Migration
```python
# "Create a migration to add updated_at column"
# The AI will use: mcp_supabase_apply_migration
```

### Check Logs
```python
# "Show me API logs from last hour"
# The AI will use: mcp_supabase_get_logs
```

## Environment Variables

Your `.env` file should contain:

```env
# Supabase Configuration (from MCP)
SUPABASE_URL=https://dyvcdtsxrwyoevgsiuwf.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5dmNkdHN4cnd5b2V2Z3NpdXdmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg4ODQ0NTYsImV4cCI6MjA3NDQ2MDQ1Nn0.8ZfhHgckN_-up_CfamMxwM7ath5mNbSie9xYr5FjsdE

# Database Connection String
# Get from Supabase Dashboard → Settings → Database
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres
```

## Next Steps

1. ✅ Code updated to use `running_articles` table
2. ⚠️ Create RLS policies for API access
3. 📝 Update `.env` with database password
4. 🚀 Test API endpoints

## Using MCP in Cursor

Simply ask the AI assistant:
- "Query the running_articles table using MCP"
- "Create a migration to add a new column"
- "Show me database logs"
- "Generate TypeScript types for my schema"

The AI will automatically use the appropriate MCP tools!

