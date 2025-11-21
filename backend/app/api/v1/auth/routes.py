from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.users_service import UsersService
from .schemas import UserCreate, UserLogin, Token, UserOut
from .dependencies import get_current_user
from .models import User
from app.database.session import get_db

router = APIRouter()

# Função que trunca a senha para no máximo 72 bytes (limite do bcrypt).
def _truncate_password(password: str, max_bytes: int = 72) -> str:
	b = password.encode("utf-8")
	if len(b) <= max_bytes:
		return password
	truncated = b[:max_bytes]
	# decodifica descartando bytes inválidos no final de um caractere multibyte
	return truncated.decode("utf-8", errors="ignore")

# Fallbacks para hashing/verificação usando o pacote bcrypt diretamente.
def _get_hash_verify_funcs():
	"""
	Retorna (hash_password, verify_password, create_access_token_or_none)
	- Tenta importar de app.auth.utils;
	- Se falhar por causa do passlib/bcrypt, fornece fallback para hash/verify usando bcrypt.
	"""
	try:
		from .utils import hash_password, verify_password, create_access_token
		return hash_password, verify_password, create_access_token
	except Exception:
		# Import tardio do bcrypt e implementação simples de fallback
		try:
			import bcrypt
		except Exception as ie:
			# Não conseguimos usar bcrypt nem utils -> re-lançar para tratamento no endpoint
			raise RuntimeError("bcrypt unavailable and app.auth.utils import failed") from ie

		def _hash_password(pw: str) -> str:
			h = bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt())
			return h.decode("utf-8")

		def _verify_password(pw: str, hashed: str) -> bool:
			try:
				return bcrypt.checkpw(pw.encode("utf-8"), hashed.encode("utf-8"))
			except Exception:
				return False

		# create_access_token pode não estar disponível — retornamos None para sinalizar isso
		return _hash_password, _verify_password, None

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
	# truncate antes de hashear para evitar o erro de >72 bytes
	truncated_pwd = _truncate_password(user.password)

	# obter funcs (lazy import). Se ambos falharem, devolve 500 claro.
	try:
		hash_password, _, _ = _get_hash_verify_funcs()
	except RuntimeError:
		raise HTTPException(status_code=500, detail="Password hashing not available; check bcrypt/passlib installation")

	if db.query(User).filter(User.email == user.email).first():
		raise HTTPException(status_code=400, detail="Email already registered")
	new_user = User(
		email=user.email,
		hashed_password=hash_password(truncated_pwd),
		vbucks=10000
	)
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
	db_user = db.query(User).filter(User.email == user.email).first()
	# truncate antes de verificar para usar a mesma cadeia de bytes que foi hasheada
	truncated_pwd = _truncate_password(user.password)

	# obter funcs (lazy import). Também tentamos obter create_access_token.
	try:
		_, verify_password, create_access_token = _get_hash_verify_funcs()
	except RuntimeError:
		raise HTTPException(status_code=500, detail="Password verification not available; check bcrypt/passlib installation")

	if not db_user or not verify_password(truncated_pwd, db_user.hashed_password):
		raise HTTPException(status_code=401, detail="Invalid credentials")

	if create_access_token is None:
		# Se create_access_token não pôde ser importado, pedir que o servidor seja corrigido.
		raise HTTPException(status_code=500, detail="Token creation not available; check auth utils configuration")

	token = create_access_token({"sub": str(db_user.id)})
	return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
	return current_user