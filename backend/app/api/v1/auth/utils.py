from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "fortnite-cosmetics-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def _truncate_password(password: str, max_bytes: int = 72) -> str:
    b = password.encode("utf-8")
    if len(b) <= max_bytes:
        return password
    truncated = b[:max_bytes]
    return truncated.decode("utf-8", errors="ignore")

def hash_password(password: str) -> str:
    """
    Hash usando o pacote `bcrypt` diretamente. Garante truncamento seguro a 72 bytes.
    Retorna hash como str (utf-8).
    """
    try:
        import bcrypt
    except Exception as e:
        # falha clara para troubleshooting
        raise RuntimeError("bcrypt is required for password hashing") from e

    pw = _truncate_password(password).encode("utf-8")
    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    """
    Verifica senha usando bcrypt.checkpw; aplica truncamento idêntico ao hashing.
    Retorna False em qualquer erro de verificação.
    """
    try:
        import bcrypt
    except Exception:
        return False

    pw = _truncate_password(password).encode("utf-8")
    try:
        return bcrypt.checkpw(pw, hashed.encode("utf-8"))
    except Exception:
        return False

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)