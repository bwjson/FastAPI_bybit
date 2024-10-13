from celery import Celery
from celery.schedules import timedelta
from src.config import REDIS_HOST, REDIS_PORT
from .dependencies import transaction_service

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')

celery.conf.beat_schedule = {
    'run-add-every-10-seconds': {
        'task': 'src.transaction.tasks.check_match',
        'schedule': timedelta(seconds=10),
    }
}

celery.conf.timezone = 'UTC'

@celery.task
def send_email():
	...
	
    
