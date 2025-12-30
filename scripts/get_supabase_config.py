"""
Helper script to get Supabase configuration via MCP
Run this script to get your Supabase credentials for .env file
"""
import json

# Note: This script demonstrates the values you need for .env
# The actual MCP connection is handled by Cursor's MCP integration

print("=" * 60)
print("Supabase Configuration for .env file")
print("=" * 60)
print()
print("Your Supabase Project URL:")
print("https://dyvcdtsxrwyoevgsiuwf.supabase.co")
print()
print("Your Supabase Keys:")
print("SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR5dmNkdHN4cnd5b2V2Z3NpdXdmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg4ODQ0NTYsImV4cCI6MjA3NDQ2MDQ1Nn0.8ZfhHgckN_-up_CfamMxwM7ath5mNbSie9xYr5FjsdE")
print()
print("Database Connection String:")
print("Format: postgresql://postgres:[YOUR-PASSWORD]@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres")
print()
print("=" * 60)
print("To get your database password:")
print("1. Go to Supabase Dashboard")
print("2. Settings → Database")
print("3. Copy the connection string")
print("=" * 60)

