from celery import Celery
from app.services import fortnite

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def sync_cosmetics():
    from app.database import SessionLocal
    from app.models import Cosmetic
    db = SessionLocal()
    data = fortnite.fetch_cosmetics()