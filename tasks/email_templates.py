from email.message import EmailMessage

from config import settings


class CreateNews:
    def __init__(self, title: str):
        self.title = title

    def create_news(
            self,
            content: dict,
            email_to: EmailMessage,
    ):
        email = EmailMessage()
        email['Subject'] = f'Interesting news about {self.title}'
        email['From'] = settings.SMTP_USER
        email['To'] = email_to
        email.set_content(
            f"""
                <h1>Interesting news</h1>
                {content}
            """,
            subtype='html',
        )
        return email
