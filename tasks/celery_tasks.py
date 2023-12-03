import smtplib
from email.message import EmailMessage

from PIL import Image
from pathlib import Path

from celery import Celery
from pydantic import EmailStr

from config import settings
from tasks.celeryconfig import celery_config
from tasks.email_templates import CreateNews

celery = Celery(
    'tasks',
    # backend=settings.redis_url,
    # broker=settings.redis_url,
    # include=['tasks.celery_tasks']
)

celery.config_from_object(celery_config, namespace='CELERY')


@celery.task(ignore_result=True)
def process_pic(
        path: str,
):
    image_path = Path(path)
    image = Image.open(path)
    image_resized_1000_500 = image.resize((1000, 500))
    image_resized_200_100 = image.resize((200, 100))
    image_resized_1000_500.save(f'static/images/resized_1000_500_{image_path.name}')
    image_resized_200_100.save(f'static/images/resized_200_100_{image_path.name}')


@celery.task
def send_news(title: str, content: dict, email_to: EmailStr):
    email_to_mock = settings.SMTP_USER
    create_news = CreateNews(title=title)
    msg_content = create_news.create_news(
        content=content,
        email_to=email_to_mock,
    )
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
