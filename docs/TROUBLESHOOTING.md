# Troubleshooting Guide

## DNS Resolution Error: `getaddrinfo failed`

If you see this error:
```
socket.gaierror: [Errno 11001] getaddrinfo failed
```

This means your computer can't resolve the database hostname. Here's how to fix it:

### Solution 1: Verify DATABASE_URL Format

Your `.env` file should have the correct format. Check:

**Correct format:**
```env
DATABASE_URL=postgresql://postgres:your_encoded_password@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres
```

**Common mistakes:**
- ❌ Missing `postgresql://` prefix
- ❌ Wrong hostname (should be `db.dyvcdtsxrwyoevgsiuwf.supabase.co`)
- ❌ Wrong port (should be `5432`)
- ❌ Password not URL-encoded (special characters like `##` need encoding)

### Solution 2: Use Connection Pooling URL (Recommended)

Supabase provides connection pooling URLs that are more reliable:

**Transaction Mode (for serverless/API):**
```env
DATABASE_URL=postgresql://postgres.dyvcdtsxrwyoevgsiuwf:your_encoded_password@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
```

**Session Mode:**
```env
DATABASE_URL=postgresql://postgres.dyvcdtsxrwyoevgsiuwf:your_encoded_password@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
```

To get your exact pooling URL:
1. Go to Supabase Dashboard → Settings → Database
2. Scroll to "Connection string"
3. Select "Connection pooling" tab
4. Copy the URI (use Transaction mode for APIs)

### Solution 3: Check Network/DNS

1. **Test DNS resolution:**
   ```bash
   ping db.dyvcdtsxrwyoevgsiuwf.supabase.co
   ```

2. **Check firewall/antivirus** - They might be blocking the connection

3. **Try using IP address** (if available from Supabase dashboard)

### Solution 4: Verify Password Encoding

If your password contains `##`, make sure it's encoded as `%23%23`:

**Example:**
- Password: `mypass##123`
- Encoded: `mypass%23%23123`
- Full URL: `postgresql://postgres:mypass%23%23123@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres`

### Solution 5: Test Connection Directly

Use the test script:
```bash
python scripts/test_connection.py
```

Or test with psql (if installed):
```bash
psql "postgresql://postgres:your_password@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres"
```

## Other Common Errors

### Error: "password authentication failed"
- ✅ Verify password is correct
- ✅ Check if password needs URL encoding
- ✅ Ensure you're using the `postgres` user password (not API key)

### Error: "connection refused"
- ✅ Check Supabase project is active
- ✅ Verify your IP is allowed (Settings → Database → Connection pooling)
- ✅ Check if using correct port (5432 for direct, 6543 for pooling)

### Error: "does not appear to be an IPv4 or IPv6 address"
- ✅ Replace `[YOUR-PASSWORD]` placeholder with actual password
- ✅ URL-encode special characters in password

## Quick Test

Run this to verify your connection string format:
```python
from urllib.parse import urlparse
url = "your_DATABASE_URL_here"
parsed = urlparse(url)
print(f"Scheme: {parsed.scheme}")
print(f"User: {parsed.username}")
print(f"Host: {parsed.hostname}")
print(f"Port: {parsed.port}")
print(f"Database: {parsed.path.lstrip('/')}")
```

All values should be populated correctly!

