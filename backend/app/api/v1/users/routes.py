from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, Header
from sqlalchemy.orm import Session

# Database e Core
from app.database.session import get_db
from app.celery.config import celery_app

# Services e Models
from app.services.user_service import UserService
from .models import User
from .schemas import UserCreate, UserLogin, Token, UserOut
from .dependencies import get_current_user

router = APIRouter()

# --- UTILS INTERNOS (Hashing & Truncate) ---

def _truncate_password(password: str, max_bytes: int = 72) -> str:
    """Trunca a senha para o limite do bcrypt (72 bytes)."""
    b = password.encode("utf-8")
    if len(b) <= max_bytes:
        return password
    return b[:max_bytes].decode("utf-8", errors="ignore")

def _get_auth_funcs():
    """Tenta importar utilitários de auth ou fornece fallbacks."""
    try:
        from auth.utils import hash_password, verify_password, create_access_token
        return hash_password, verify_password, create_access_token
    except Exception:
        try:
            import bcrypt
            def _hash(pw: str) -> str:
                return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            def _verify(pw: str, hashed: str) -> bool:
                return bcrypt.checkpw(pw.encode("utf-8"), hashed.encode("utf-8"))
            return _hash, _verify, None
        except ImportError:
            raise RuntimeError("Dependências de criptografia não encontradas.")

# --- ROTAS DE AUTENTICAÇÃO ---

@router.post("/register", response_model=UserOut, tags=["Autenticação"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    hash_pwd, _, _ = _get_auth_funcs()
    
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    truncated_pwd = _truncate_password(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hash_pwd(truncated_pwd),
        vbucks=10000
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token, tags=["Autenticação"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    _, verify_pwd, create_token = _get_auth_funcs()

    truncated_pwd = _truncate_password(user.password)
    if not db_user or not verify_pwd(truncated_pwd, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if not create_token:
        raise HTTPException(status_code=500, detail="Gerador de Token indisponível")

    token = create_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut, tags=["Autenticação"])
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

# --- ROTAS DE PERFIL E LISTAGEM (Antigo Users) ---

@router.get("", response_model=List[dict], tags=["Usuários"])
def list_users(
    page: int = Query(1, ge=1), 
    per_page: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db)
):
    """Lista paginada de usuários (id, email)."""
    return UserService.list_users(db, page=page, per_page=per_page)

@router.get("/{user_id}", response_model=dict, tags=["Usuários"])
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Perfil público com inventário de cosméticos."""
    try:
        return UserService.get_user_profile(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --- ROTA DE ADMINISTRAÇÃO (Sincronização) ---

@router.post("/admin/sync", tags=["Admin"])
async def trigger_sync(x_admin_key: str = Header(None)):
    """Dispara a sincronização de cosméticos via Celery."""
    # Substitua pela sua chave real ou use uma variável de ambiente
    if x_admin_key != "sua_chave_secreta_aqui":
        raise HTTPException(status_code=403, detail="Acesso administrativo negado")
    
    celery_app.send_task("sync_cosmetics")
    return {"status": "success", "message": "Tarefa de sincronização enviada."}