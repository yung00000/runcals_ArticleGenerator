"""
Helper script to URL-encode database passwords for DATABASE_URL
"""
from urllib.parse import quote

def encode_password(password: str) -> str:
    """
    URL-encode a password for use in DATABASE_URL
    
    Args:
        password: The database password
        
    Returns:
        URL-encoded password
    """
    return quote(password, safe='')

if __name__ == "__main__":
    print("=" * 60)
    print("Password URL Encoder for DATABASE_URL")
    print("=" * 60)
    print()
    
    # Example with ##
    example_password = "mypass##123"
    encoded = encode_password(example_password)
    
    print(f"Example Password: {example_password}")
    print(f"URL Encoded:      {encoded}")
    print()
    print("Full DATABASE_URL example:")
    print(f"postgresql://postgres:{encoded}@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres")
    print()
    print("=" * 60)
    print("To encode your own password:")
    print("1. Run: python scripts/encode_password.py")
    print("2. Or use Python:")
    print("   from urllib.parse import quote")
    print("   quote('your_password', safe='')")
    print("=" * 60)
    
    # Interactive mode
    print()
    try:
        user_password = input("Enter your password to encode (or press Enter to skip): ")
        if user_password:
            encoded_password = encode_password(user_password)
            print()
            print(f"Your encoded password: {encoded_password}")
            print()
            print("Add this to your .env file:")
            print(f"DATABASE_URL=postgresql://postgres:{encoded_password}@db.dyvcdtsxrwyoevgsiuwf.supabase.co:5432/postgres")
    except KeyboardInterrupt:
        print("\n\nCancelled.")

