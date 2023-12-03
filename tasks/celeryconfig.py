from config import settings


class CeleryConfig:
    broker_url = settings.redis_url
    result_backend = settings.redis_url
    include: list = ['tasks.celery_tasks']
    result_expires = 60
    broker_connection_retry = True
    broker_connection_retry_on_startup = True
    broker_connection_max_retries = 10


celery_config = CeleryConfig()
