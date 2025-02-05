from celery import Celery

from config import settings

REDIS_URL = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

celery_app = Celery(
    "celery_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    enable_utc=True,
    timezone=settings.TIMEZONE,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)
