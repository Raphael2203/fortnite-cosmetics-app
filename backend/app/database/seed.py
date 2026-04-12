from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.v1.users.models import User
from app.api.v1.users.utils import hash_password
from app.api.v1.purchases.models import Purchase

def maintenance_and_seed_db(db: Session):
    """
    Limpa todos os dados de usuários e compras (Reset) 
    e recria o usuário admin padrão.
    """
    try:
        print("--- INICIANDO MANUTENÇÃO DO BANCO (RESET 24H) ---")
        db.execute(text("TRUNCATE TABLE purchases, users RESTART IDENTITY CASCADE;"))
        
        email_teste = "admin@admin.com"
        test_user = User(
            email=email_teste,
            hashed_password=hash_password("admin123"),
            vbucks=10000
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"Sistema resetado. Usuário {email_teste} recriado com sucesso!")
        
    except Exception as e:
        db.rollback()
        print(f"Erro durante a manutenção: {str(e)}")
    finally:
        db.close()