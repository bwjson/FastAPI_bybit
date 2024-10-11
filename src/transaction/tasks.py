from celery import Celery
from config import REDIS_HOST, REDIS_PORT

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')

@celery.task
def add(x, y):
	print(x + y)