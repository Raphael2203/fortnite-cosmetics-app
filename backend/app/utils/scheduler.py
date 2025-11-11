from celery.schedules import crontab
from worker import celery_app

celery_app.conf.beat_schedule = {
    "sync-every-6-hours": {
        "task": "worker.sync_cosmetics",
        "schedule": crontab(minute=0, hour="*/6"),
    }
}