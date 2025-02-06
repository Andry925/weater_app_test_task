from celery import Celery
from decouple import config

from config import settings

OPENAI_API_KEY = config('OPENAI_API_KEY')

REDIS_URL = f"redis://redis:6379/0"

celery_app = Celery(
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['tasks.process_input_task']

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

celery_app.autodiscover_tasks()
