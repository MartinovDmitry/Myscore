from email.message import EmailMessage

from config import settings


class CreateNews:
    def __init__(self, class_obj):
        self.class_obj = class_obj

    def create_news(
            self,
            content: dict,
            email_to: EmailMessage,
    ):
        email = EmailMessage()
        email['Subject'] = f'News abot {self.class_obj.__tablename__}'
        email['From'] = settings.SMTP_USER
        email['To'] = email_to
        email.set_content(
            f"""
                <h1>{self.class_obj.__tablename__.title()} news</h1>
                {content}
            """,
            subtype='html',
        )
        return email
