from email.message import EmailMessage

from config import settings


def create_leagues_news(
        leagues: dict,
        email_to: EmailMessage,
):
    email = EmailMessage()
    email['Subject'] = 'News about leagues'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to
    email.set_content(
        f"""
            <h1>Leagues new</h1>
            {leagues}
        """,
        subtype='html',
    )
