# Fix DNS Resolution Error (getaddrinfo failed)

## Problem
Your application cannot resolve the database hostname `db.dyvcdtsxrwyoevgsiuwf.supabase.co`, causing DNS resolution failure.

## Solution: Use Connection Pooling URL

The **Connection Pooling URL** is more reliable and recommended for API applications. It uses a different hostname that's more likely to resolve correctly.

### Step-by-Step Fix

#### 1. Get Your Connection Pooling URL

1. Open Supabase Dashboard:
   ```
   https://supabase.com/dashboard/project/dyvcdtsxrwyoevgsiuwf
   ```

2. Go to **Settings** → **Database**

3. Scroll down to **"Connection string"** section

4. Click on **"Connection pooling"** tab (NOT "URI")

5. Select **"Transaction"** mode (recommended for APIs)

6. Copy the **URI** connection string

#### 2. Update Your .env File

Replace your current `DATABASE_URL` with the pooling URL:

**Before (Direct Connection - causing DNS error):**
```env
DATABASE_URL=postgresql://postgres:password@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres
```

**After (Connection Pooling - Transaction Mode - recommended for APIs):**
```env
DATABASE_URL=postgres://postgres:password@db.dyvcdtsxrwyoevgsiuwf.supabase.co:6543/postgres
```

**Or Session Mode (for persistent connections):**
```env
DATABASE_URL=postgres://postgres.dyvcdtsxrwyoevgsiuwf:password@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
```

**Important Notes:**
- **Transaction Mode (port 6543)**: Best for APIs/serverless - automatically handled by code
- **Session Mode (port 5432)**: Best for persistent connections - requires region in hostname
- Replace `password` with your actual password
- If password contains `##`, encode it as `%23%23`
- If password contains `$`, encode it as `%24`
- Transaction mode doesn't support prepared statements (code handles this automatically)

#### 3. Example with Encoded Password

If your password is `mypass##123`:

```env
DATABASE_URL=postgresql://postgres.dyvcdtsxrwyoevgsiuwf:mypass%23%23123@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
```

#### 4. Restart Your Server

```bash
uvicorn app.main:app --reload
```

## Why Connection Pooling?

✅ **More reliable DNS resolution**  
✅ **Better for serverless/API applications**  
✅ **Handles connection pooling automatically**  
✅ **Same security and performance**

## Alternative: Check Your Network

If you still have issues:

1. **Check DNS settings:**
   ```bash
   nslookup db.dyvcdtsxrwyoevgsiuwf.supabase.co
   ```

2. **Try different DNS server:**
   - Use Google DNS: `8.8.8.8` or `8.8.4.4`
   - Or Cloudflare DNS: `1.1.1.1`

3. **Check firewall/antivirus:**
   - Temporarily disable to test
   - Add exception for Python/uvicorn

4. **Use VPN:**
   - Some networks block database connections
   - Try connecting via VPN

## Quick Test Script

Run this to check your connection:
```bash
python scripts/check_connection_options.py
```

This will show your current configuration and help identify issues.

