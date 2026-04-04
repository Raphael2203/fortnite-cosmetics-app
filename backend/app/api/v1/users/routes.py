from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, Header
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.celery.config import celery_app
from app.services.user_service import UserService

from .models import User
from .schemas import UserCreate, UserLogin, Token, UserOut
from .dependencies import get_current_user
from .utils import hash_password, verify_password, create_access_token

router = APIRouter()

def _truncate_password(password: str, max_bytes: int = 72) -> str:
    b = password.encode("utf-8")
    if len(b) <= max_bytes:
        return password
    return b[:max_bytes].decode("utf-8", errors="ignore")

@router.post("/register", response_model=UserOut, tags=["Autenticação"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    truncated_pwd = _truncate_password(user.password)
    
    new_user = User(
        email=user.email,
        hashed_password=hash_password(truncated_pwd),
        vbucks=10000
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token, tags=["Autenticação"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    truncated_pwd = _truncate_password(user.password)

    if not db_user or not verify_password(truncated_pwd, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut, tags=["Autenticação"])
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("", response_model=List[dict], tags=["Usuários"])
def list_users(
    page: int = Query(1, ge=1), 
    per_page: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db)
):
    return UserService.list_users(db, page=page, per_page=per_page)

@router.get("/{user_id}", response_model=dict, tags=["Usuários"])
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    try:
        return UserService.get_user_profile(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/admin/sync", tags=["Admin"])
async def trigger_sync(x_admin_key: str = Header(None)):
    if x_admin_key != "fortnite-cosmetics-app":
        raise HTTPException(status_code=403, detail="Acesso administrativo negado")
    
    celery_app.send_task("sync_cosmetics")
    return {"status": "success", "message": "Tarefa de sincronização enviada."}