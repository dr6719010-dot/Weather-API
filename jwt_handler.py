from jose import jwt
from datetime import datetime, timedelta, timezone
from exceptions import JWTCustomError, InvalidTokenError
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRY_MINUTES = 60

def create_token(data: dict) -> str:
    """Create a JWT containing the given data, with an expiry."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """Decode and verify a JWT. Raises an exception if invalid or expired."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTCustomError:
        raise InvalidTokenError("invalid or expired token")
