from sqlalchemy.orm import Session
from app.api.v1.users.models import User
from app.api.v1.users.utils import hash_password

def seed_test_user(db: Session):
    email_teste = "admin@admin.com"
    user_exists = db.query(User).filter(User.email == email_teste).first()

    if not user_exists:
        print("Criando usuário de semente (seed)...")
        test_user = User(
            email=email_teste,
            hashed_password=hash_password("admin123"), # Senha padrão
            vbucks=10000
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"Usuário {email_teste} criado com sucesso!")
    else:
        print("Usuário de semente já existe no banco.")