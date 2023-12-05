from kombu import Queue

from config import settings


class CeleryConfig:
    broker_url = settings.redis_url
    result_backend = settings.redis_url
    include: list = ['tasks.celery_tasks', 'tasks.schedule_tasks']
    # enable_utc = True
    # timezone = 'Europe/London'
    task_default_queue = 'celery'
    task_queues = (
        Queue(name='celery', routing_key=None),
        Queue(name='celery-queue-news', routing_key='news'),
        Queue(name='celery-queue-images', routing_key='images'),
    )
    task_routes = {
        'tasks.celery_tasks.process_pic': {
            # check parameter 'ignore_result=True' in decorator
            'queue': 'celery-queue-images',
            'routing_key': 'images',
        }
    }
    result_expires = 60
    broker_connection_retry = True
    broker_connection_retry_on_startup = True
    broker_connection_max_retries = 10
    beat_schedule = {
        'add-connection-every-10-seconds': {
            'task': 'tasks.schedule_tasks.checking_connection',
            'schedule': 10,
            'args': (1, 2,),
        }
    }


celery_config = CeleryConfig()
