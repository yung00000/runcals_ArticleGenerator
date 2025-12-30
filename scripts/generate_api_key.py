"""
Generate a secure API key for use in .env file
"""
import secrets

def generate_api_key(length: int = 32) -> str:
    """
    Generate a secure random API key
    
    Args:
        length: Length of the key in bytes (default: 32)
        
    Returns:
        URL-safe base64 encoded random string
    """
    return secrets.token_urlsafe(length)


if __name__ == "__main__":
    print("=" * 70)
    print("API Key Generator")
    print("=" * 70)
    print()
    
    # Generate API key
    api_key = generate_api_key(32)
    
    print("Generated API Key:")
    print(f"  {api_key}")
    print()
    print("Add this to your .env file:")
    print(f"  API_KEY={api_key}")
    print()
    print("=" * 70)
    print("Security Notes:")
    print("- Keep this key secret and never commit it to version control")
    print("- Use different keys for development and production")
    print("- Rotate keys regularly for better security")
    print("=" * 70)

