from celery import Celery
from celery.schedules import crontab
from app.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_app = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["celery_app.tasks"]
)

celery_app.conf.update(
    timezone="America/Sao_Paulo",
    enable_utc=False,
    beat_schedule={
        "sync-every-6-hours": {
            "task": "celery_app.tasks.sync_cosmetics",
            "schedule": crontab(minute=0, hour="*/6"),
        }
    }
)