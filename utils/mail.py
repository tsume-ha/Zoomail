from django.conf import settings
from enum import Enum

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    To,
    PlainTextContent,
)

from mail.models import SendMailAddress, MailLog


class MailStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class SendGridClient(SendGridAPIClient):
    def __init__(self) -> None:
        api_key = settings.SENDGRID_API_KEY
        super(SendGridClient, self).__init__(api_key)


class SympleMessageSendClient(SendGridClient):
    def __init__(self, title: str, text: str, to_email: str, from_email: str):
        super().__init__()
        self.title = title
        self.text = text
        self.from_email = from_email
        self.to_email = to_email

    def send(self):
        status = MailStatus.PENDING
        error_msg = ""
        try:
            response = super().send(
                Mail(
                    from_email=self.from_email,
                    to_emails=[To(email=self.to_email)],
                    reply_to=None,
                    subject=self.title,
                    plain_text_content=PlainTextContent(self.text),
                    html_content=None,
                    amp_html_content=None,
                    global_substitutions=None,
                    is_multiple=False,
                )
            )
            x_message_id = response.headers["X-Message-Id"]
            status = MailStatus.SUCCESS
        except Exception as e:
            x_message_id = ""
            status = MailStatus.FAILED
            error_msg = str(e)
        finally:
            MailLog.objects.create(
                message=None,
                mail_id=x_message_id,
                email=self.to_email,
                user=None,
                send_server=MailLog.SendServerChoices.SENDGRID,
                status=status,
                error=error_msg,
            )
        return response
