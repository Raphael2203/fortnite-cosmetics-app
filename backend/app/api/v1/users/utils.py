from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "fortnite-cosmetics-app")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def _truncate_password(password: str, max_bytes: int = 72) -> str:
    b = password.encode("utf-8")
    if len(b) <= max_bytes:
        return password
    return b[:max_bytes].decode("utf-8", errors="ignore")

def hash_password(password: str) -> str:
    import bcrypt
    pw = _truncate_password(password).encode("utf-8")
    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    import bcrypt
    try:
        pw = _truncate_password(password).encode("utf-8")
        return bcrypt.checkpw(pw, hashed.encode("utf-8"))
    except Exception:
        return False

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)