from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Truncamento seguro para no máximo 72 bytes (limite do bcrypt)
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

# Criação de token JWT usada pelos endpoints. Usa `python-jose` (jose.jwt).
# Se o seu projeto já possuir outra implementação, substitua por ela.
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
	try:
		from jose import jwt
	except Exception as e:
		raise RuntimeError("python-jose is required to create JWT tokens") from e

	# tenta obter settings do projeto, com fallback para valores sensatos
	try:
		from app.core.config import settings
		SECRET_KEY = getattr(settings, "SECRET_KEY", "changeme")
		ALGORITHM = getattr(settings, "ALGORITHM", "HS256")
		default_expires = getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 60)
	except Exception:
		SECRET_KEY = "changeme"
		ALGORITHM = "HS256"
		default_expires = 60

	to_encode = data.copy()
	if expires_delta is None:
		expires_delta = timedelta(minutes=default_expires)
	exp = datetime.utcnow() + expires_delta
	to_encode.update({"exp": exp})
	return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)