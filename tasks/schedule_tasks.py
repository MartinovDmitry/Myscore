# This file do not work on Windows
from tasks.celery_tasks import celery


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, checking_connection.s(1, 2), name='checking-connection')


@celery.task(ignore_result=True)
def checking_connection(x, y):
    print('celery is still connected')
