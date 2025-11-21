from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.celery.tasks"]
)

celery_app.conf.update(
    timezone="America/Sao_Paulo",
    enable_utc=False,
    beat_schedule={
        "sync-every-6-hours": {
            "task": "sync_cosmetics",
            "schedule": crontab(minute=0, hour="*/6"),
        }
    }
)