from typing import List
from board.models import Message
from mail.models import SendMailAddress, MailLog
from django.conf import settings
import base64
import uuid
import requests

SEND_MAIL = settings.SEND_MAIL
SEND_MAIL_API_ENDPOINT = settings.SEND_MAIL_API_ENDPOINT
SEND_MAIL_API_ID = settings.SEND_MAIL_API_ID
SEND_MAIL_API_KEY = settings.SEND_MAIL_API_KEY


class MailContent:
    def __init__(
        self,
        subject: str = None,
        text: str = None,
        to_email: str = None,
        from_email: str = None,
        from_name: str = None,
        user=None,
    ) -> None:
        self.subject = subject
        self.text = text
        self.to_email = to_email
        self.from_email = from_email
        self.from_name = from_name
        self.user = user
        self.mail_id = str(uuid.uuid4())

    def set_subject(self, subject: str):
        self.subject = subject

    def set_text(self, text: str):
        self.text = text

    def set_to(self, email: str):
        self.to_email = email

    def set_from(self, email: str, name: str):
        self.from_email = email
        self.from_name = name

    def set_user(self, user):
        self.user = user

    def as_dict(self) -> dict:
        return {
            "subject": self.subject,
            "text": self.text,
            "to": self.to_email,
            "from": {"email": self.from_email, "name": self.from_name},
            "id": self.mail_id,
        }


class MailAttachment:
    def __init__(self) -> None:
        self.filename = None
        self.base64encoded = None

    def load_file(self, filepath, filename=None):
        if filename is not None:
            self.filename = filename
        else:
            self.filename = filepath.split("/")[-1]
        with open(filepath, "rb") as f:
            data = f.read()
            f.close()
        self.base64encoded = base64.b64encode(data).decode("utf-8")

    def as_dict(self):
        return {"filename": self.filename, "content": self.base64encoded}


class SympleMailSender:

    def __init__(self) -> None:
        self.content_list: List[MailContent] = []
        self.attachment_list: List[MailAttachment] = []

    def set_content_list(self, content_list: List[MailContent]):
        self.content_list = content_list

    def set_attachment_list(self, attachment_list: List[MailAttachment]):
        self.attachment_list = attachment_list

    def _save_mail_logs(self):
        log_list = [
            MailLog(
                mail_id=content.mail_id,
                email=content.to_email,
                user=content.user,
                send_server=MailLog.SendServerChoices.SES,
                status=MailLog.StatusChoices.PENDING,
            )
            for content in self.content_list
        ]
        MailLog.objects.bulk_create(log_list)

    def _request(self):
        data = {
            "message": [content.as_dict() for content in self.content_list],
            "attachments": [attachment.as_dict() for attachment in self.attachment_list],
        }
        headers = {"x-api-key": SEND_MAIL_API_KEY, "x-api-id": SEND_MAIL_API_ID, "Content-Type": "application/json"}
        response = requests.post(url=SEND_MAIL_API_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()

    def send(self):
        if SEND_MAIL:
            self._save_mail_logs()
            self._request()
            return len(self.content_list)
        else:
            return 0


class MailisSender(SympleMailSender):

    def __init__(self, message: Message):
        super().__init__()
        self.message = message

        # メール内容を設定
        if message.years.filter(year=0).exists():
            send_address_list = SendMailAddress.objects.all()
            content_list = [
                MailContent(
                    subject=message.title,
                    text=message.content
                    + "\n\n--------------------------------\nこのメーリスのURLはこちら\nhttps://zoomail.ku-unplugged.net/mail/"
                    + str(message.pk),
                    to_email=address.email,
                    from_email="zenkai@zoomail.ku-unplugged.net",
                    from_name=message.writer.get_short_name(),
                    user=address.user,
                )
                for address in send_address_list
            ]
            super().set_content_list(content_list)
        else:
            content_list = []
            for year in message.years.all().values_list("year", flat=True):
                send_address_list = SendMailAddress.objects.filter(user__year=year)
                content_list += [
                    MailContent(
                        subject=message.title,
                        text=message.content
                        + "\n\n--------------------------------\nこのメーリスのURLはこちら\nhttps://zoomail.ku-unplugged.net/mail/"
                        + str(message.pk),
                        to_email=address.email,
                        from_email=f"{year - 1994}kaisei@zoomail.ku-unplugged.net",
                        user=address.user,
                    )
                    for address in send_address_list
                ]
            super().set_content_list(content_list)

        # 添付ファイルを設定
        attachment_list = []
        for attachment in message.attachments.all():
            file = MailAttachment()
            file.load_file(attachment.attachment_file.path)
            attachment_list.append(file)
        if len(attachment_list):
            super().set_attachment_list(attachment_list)

    def _save_mail_logs(self):
        log_list = [
            MailLog(
                message=self.message,
                mail_id=content.mail_id,
                email=content.to_email,
                user=content.user,
                send_server=MailLog.SendServerChoices.SES,
                status=MailLog.StatusChoices.PENDING,
            )
            for content in self.content_list
        ]
        MailLog.objects.bulk_create(log_list)
