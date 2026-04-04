from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# Importações corrigidas para a nova estrutura interna de 'users'
from .models import User
from .utils import SECRET_KEY, ALGORITHM # Busca do utils que está na mesma pasta
from app.database.session import get_db

# O tokenUrl deve apontar para a rota de login relativa ao prefixo da API.
# Como agora tudo está em /users, o Swagger buscará em /api/v1/users/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Valida o token JWT e retorna o objeto do usuário logado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodifica o token usando as chaves do seu novo utils.py
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get("sub")
        
        if user_id_str is None:
            raise credentials_exception
            
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        # Se o token estiver corrompido ou o 'sub' não for um ID válido
        raise credentials_exception

    # Busca o usuário no banco de dados
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado"
        )
        
    return user