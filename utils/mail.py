import base64

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, PlainTextContent, Attachment, FileContent, FileName, FileType, Disposition

from django.conf import settings

from board.models import Message
from mail.models import SendMailAddress, MessageProcess

class SendGridClient(SendGridAPIClient):
    def __init__(self) -> None:
        self.api_key = settings.SENDGRID_API_KEY
        self.mail = None
        super(SendGridClient, self).__init__(self.api_key)

    def send(self, message):
        response = super().send(message)
        return response




class SendgridMail(Mail):    
    def __init__(self, message: Message, year: int):
        self.message = message
        self.year = year
        self.from_email = self.__generate_from_email()
        self.to_emails = self.__generate_to_emails()
        self.plain_text_content = self.__generate_plain_text_content()

        super().__init__(
            from_email=self.from_email,
            to_emails=self.to_emails,
            reply_to=None,
            subject=message.title,
            plain_text_content=self.plain_text_content,
            html_content=None,
            amp_html_content=None,
            global_substitutions=None,
            is_multiple=True
            )

        attachments = self.message.attachments.order_by('id').reverse()
        for attachment in attachments:
            file_path = attachment.attachment_file.path
            with open(file_path, 'rb') as f:
                a_data = f.read()
                f.close()
            encoded = base64.b64encode(a_data).decode()
            attachment_file = Attachment(
                file_content = FileContent(encoded),
                file_type = FileType('application/octet-stream'),
                file_name = FileName(attachment.fileName()),
                disposition = Disposition('attachment'),
                )
            super().add_attachment(attachment_file)


    def __generate_from_email(self):
        if self.year == 0:
            from_adress = 'zenkai@message.ku-unplugged.net'
            return (from_adress, self.message.writer.get_short_name())
        else:
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
            from_adress = ordinal(self.year - 1994) + '_kaisei@message.ku-unplugged.net'
            return (from_adress, self.message.writer.get_short_name())
            
    def __generate_to_emails(self):
        if self.year == 0:
            to_list = SendMailAddress.objects.all().values_list('email', flat=True)
        else:
            to_list = SendMailAddress.objects.filter(year=self.year).values_list('email', flat=True)
        return [To(email=eml) for eml in to_list]

    def __generate_plain_text_content(self):
        ADD_TEXT = '\n\n--------------------------------\nこのメッセージのURLはこちら\nhttps://message.ku-unplugged.net/read/content/' + str(self.message.pk)
        original_text = self.message.content
        return PlainTextContent(original_text + ADD_TEXT)


def MailingList(message: Message):
    """
    message -> board.models.Message object
    """
    to_years = message.years.all()
    if to_years.filter(year=0).exists():
        return [SendgridMail(message=message, year=0), ]
    else:
        to_years.exclude(year=0)
        return [SendgridMail(message=message, year=y.year) for y in to_years]