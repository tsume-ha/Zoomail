from typing import List, Optional
import mimetypes

import boto3
from django.conf import settings
from email.message import EmailMessage
from email.utils import formataddr, parseaddr

AWS_SES_REGION_NAME = settings.AWS_SES_REGION_NAME
AWS_SES_ACCESS_KEY = settings.AWS_SES_ACCESS_KEY
AWS_SES_SECRET_KEY = settings.AWS_SES_SECRET_KEY


def build_raw_mail(
    from_email: str,
    from_name: str,
    to_emails: List[str],
    subject: str,
    text_content: str,
    html_content: Optional[str],
    attachments,
) -> EmailMessage:
    mail = EmailMessage()
    mail["Subject"] = subject
    mail["From"] = formataddr((from_name, from_email), charset="utf-8")
    mail["To"] = ", ".join(to_emails)
    mail.set_content(text_content, subtype="plain", charset="utf-8")
    if html_content is not None:
        mail.add_alternative(html_content, subtype="html", charset="utf-8")
    if attachments is not None:
        for attachment in attachments:
            with open(attachment.attachment_file.path, "rb") as f:
                a_data = f.read()
                f.close()
            minetype = mimetypes.guess_type(attachment.attachment_file.path)[0]
            mail.add_attachment(
                a_data,
                maintype=minetype.split("/")[0],
                subtype=minetype.split("/")[1],
                filename=attachment.fileName(),
            )
    return mail


class SESSender:
    client = boto3.client(
        "ses",
        region_name=AWS_SES_REGION_NAME,
        aws_access_key_id=AWS_SES_ACCESS_KEY,
        aws_secret_access_key=AWS_SES_SECRET_KEY,
    )

    def send(self, mail: EmailMessage):
        response = self.client.send_raw_email(
            Source=parseaddr(mail["From"])[1],
            Destinations=mail.get_all("To"),
            RawMessage={"Data": mail.as_bytes()},
        )
        return response
