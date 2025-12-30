"""
Helper script to check database connection options
"""
import os
from urllib.parse import urlparse

print("=" * 70)
print("Database Connection Troubleshooting")
print("=" * 70)
print()

# Check if .env file exists
env_file = ".env"
if os.path.exists(env_file):
    print("[OK] Found .env file")
    
    # Try to read DATABASE_URL
    try:
        with open(env_file, 'r') as f:
            content = f.read()
            if 'DATABASE_URL' in content:
                # Extract DATABASE_URL
                for line in content.split('\n'):
                    if line.startswith('DATABASE_URL='):
                        db_url = line.split('=', 1)[1].strip()
                        parsed = urlparse(db_url)
                        print(f"\nCurrent DATABASE_URL configuration:")
                        print(f"  Host: {parsed.hostname}")
                        print(f"  Port: {parsed.port}")
                        print(f"  User: {parsed.username}")
                        print(f"  Database: {parsed.path.lstrip('/')}")
                        print(f"  Has Password: {'Yes' if parsed.password else 'No'}")
                        
                        # Check for placeholder
                        if '[YOUR-PASSWORD]' in db_url or '[PASSWORD]' in db_url:
                            print("\n[WARNING] Password placeholder detected!")
                            print("   Replace [YOUR-PASSWORD] with your actual password")
                        
                        # Check hostname format
                        if parsed.hostname and 'pooler.supabase.com' in parsed.hostname:
                            print("\n[OK] Using Connection Pooling URL (recommended)")
                        elif parsed.hostname and 'db.' in parsed.hostname and '.supabase.co' in parsed.hostname:
                            print("\n[WARNING] Using Direct Connection URL")
                            print("   Consider switching to Connection Pooling URL for better reliability")
                        break
            else:
                print("[WARNING] DATABASE_URL not found in .env file")
    except Exception as e:
        print(f"Error reading .env: {e}")
else:
    print("[WARNING] .env file not found")

print("\n" + "=" * 70)
print("RECOMMENDED SOLUTION: Use Connection Pooling URL")
print("=" * 70)
print()
print("1. Go to Supabase Dashboard:")
print("   https://supabase.com/dashboard/project/dyvcdtsxrwyoevgsiuwf")
print()
print("2. Navigate to: Settings → Database")
print()
print("3. Scroll to 'Connection string' section")
print()
print("4. Click on 'Connection pooling' tab")
print()
print("5. Select 'Transaction' mode (recommended for APIs)")
print()
print("6. Copy the URI connection string")
print()
print("7. Update your .env file:")
print("   DATABASE_URL=<paste_the_pooling_url_here>")
print()
print("8. Make sure to URL-encode special characters in password:")
print("   - # becomes %23")
print("   - ## becomes %23%23")
print()
print("=" * 70)
print("Example Connection Pooling URL format:")
print("=" * 70)
print("postgresql://postgres.dyvcdtsxrwyoevgsiuwf:password%23%23@")
print("aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres")
print()
print("Note: Replace 'ap-southeast-1' with your actual region")
print("      Replace 'password%23%23' with your encoded password")
print("=" * 70)

