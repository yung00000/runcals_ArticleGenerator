# Database Connection Setup Guide

## Issue: DATABASE_URL Parsing Error

If you see the error:
```
'db.dyvcdtsxrwyoevgsiuwf.supabase.co' does not appear to be an IPv4 or IPv6 address
```

This means your `.env` file still contains the placeholder `[YOUR-PASSWORD]` instead of your actual database password.

## Solution

### Step 1: Get Your Database Password

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project: `dyvcdtsxrwyoevgsiuwf`
3. Navigate to **Settings** → **Database**
4. Scroll down to **Connection string**
5. Select **URI** tab
6. Copy the connection string

### Step 2: Update .env File

Replace the `DATABASE_URL` in your `.env` file:

**Before (incorrect):**
```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres
```

**After (correct):**
```env
DATABASE_URL=postgresql://postgres:your_actual_password_here@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres
```

### Step 3: Handle Special Characters in Password

If your password contains special characters, you need to URL-encode them:

| Character | URL Encoded |
|-----------|-------------|
| `@` | `%40` |
| `#` | `%23` |
| `$` | `%24` |
| `%` | `%25` |
| `&` | `%26` |
| `+` | `%2B` |
| `=` | `%3D` |
| `?` | `%3F` |
| `/` | `%2F` |
| `:` | `%3A` |

**Examples:**

1. **Password with `##` (your case):**
   - Original: `mypass##123`
   - Encoded: `mypass%23%23123`
   - Full URL: `postgresql://postgres:mypass%23%23123@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres`

2. **Password with `@` and `#`:**
   - Original: `p@ssw#rd`
   - Encoded: `p%40ssw%23rd`
   - Full URL: `postgresql://postgres:p%40ssw%23rd@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres`

**Quick Reference:**
- `#` → `%23`
- `##` → `%23%23`
- Each `#` character must be replaced with `%23`

### Step 4: Verify Connection

After updating `.env`, restart your server:

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO - Database connection pool created successfully
```

## Alternative: Using Connection Pooling

Supabase also provides a connection pooling URL. You can use:

**Transaction Mode (recommended for serverless):**
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

**Session Mode:**
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
```

## Troubleshooting

### Error: "does not appear to be an IPv4 or IPv6 address"
- ✅ Check that `[YOUR-PASSWORD]` is replaced with actual password
- ✅ URL-encode special characters in password
- ✅ Verify the URL format is correct

### Error: "password authentication failed"
- ✅ Verify password is correct
- ✅ Check if password needs URL encoding
- ✅ Ensure you're using the correct database user (usually `postgres`)

### Error: "connection refused"
- ✅ Check if your IP is allowed in Supabase dashboard
- ✅ Verify the host and port are correct
- ✅ Check Supabase project status

## Security Best Practices

1. ⚠️ **Never commit `.env` file** to version control
2. 🔒 Use environment variables in production
3. 🛡️ Consider using Supabase connection pooling for better performance
4. 🔑 Use service role key for backend operations (more secure than anon key)

