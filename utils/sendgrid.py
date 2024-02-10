import base64
import mimetypes

from sendgrid import SendGridAPIClient
from sendgrid.helpers import mail

from django.conf import settings
from board.models import Attachment

SENDGRID_API_KEY = settings.SENDGRID_API_KEY


class SendGridClient(SendGridAPIClient):
    def __init__(self) -> None:
        api_key = SENDGRID_API_KEY
        super(SendGridClient, self).__init__(api_key)


class SendgridMail(mail.Mail):
    def __init__(
        self,
        from_email,
        to_emails,
        subject,
        plain_text_content,
        is_multiple=True,
        reply_to=None,
        html_content=None,
        amp_html_content=None,
        global_substitutions=None,
        attachments=[],
    ):
        super().__init__(
            from_email=from_email,
            to_emails=to_emails,
            reply_to=reply_to,
            subject=subject,
            plain_text_content=plain_text_content,
            html_content=html_content,
            amp_html_content=amp_html_content,
            global_substitutions=global_substitutions,
            is_multiple=is_multiple,
        )
        self.parse_attachments(attachments)

    def parse_attachments(self, attachments):
        if attachments is None:
            return None
        for attachment in attachments:
            file_path = attachment.attachment_file.path
            with open(file_path, "rb") as f:
                a_data = f.read()
                f.close()
            encoded = base64.b64encode(a_data).decode()
            attachment_file = mail.Attachment(
                file_content=mail.FileContent(encoded),
                file_name=mail.FileName(attachment.fileName()),
            )
            # disposition
            if attachment.isImage():
                attachment_file.disposition = mail.Disposition("inline")
                attachment_file.content_id = mail.ContentId(str(attachment.pk))
            else:
                attachment_file.disposition = mail.Disposition("attachment")
            # MINE type
            mine_type = mimetypes.guess_type(file_path)[0]
            if mine_type is not None:
                attachment_file.file_type = mail.FileType(mine_type)
            else:
                attachment_file.file_type = mail.FileType("application/octet-stream")
            super().add_attachment(attachment_file)
