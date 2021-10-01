import base64
import mimetypes

from django.conf import settings

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, PlainTextContent, Attachment, FileContent, FileName, FileType, Disposition, ContentId

from board.models import Message
from mail.models import SendMailAddress, MessageProcess


class ZeroTosError(Exception):
    pass

class SendGridClient(SendGridAPIClient):
    def __init__(self) -> None:
        api_key = settings.SENDGRID_API_KEY
        super(SendGridClient, self).__init__(api_key)


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
                file_name = FileName(attachment.fileName()),
                )
            # disposition
            if attachment.isImage():
                attachment_file.disposition = Disposition('inline')
                attachment_file.content_id = ContentId(str(attachment.pk))
            else:
                attachment_file.disposition = Disposition('attachment')
            # MINE type
            mine_type = mimetypes.guess_type(file_path)[0]
            if mine_type is not None:
                attachment_file.file_type = FileType(mine_type)
            else:
                attachment_file.file_type = FileType('application/octet-stream')
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

        if len(to_list) == 0:
            raise ZeroTosError('宛先が0件です。メールは送信されませんでした。')

        return [To(email=eml) for eml in to_list]

    def __generate_plain_text_content(self):
        ADD_TEXT = '\n\n--------------------------------\nこのメッセージのURLはこちら\nhttps://message.ku-unplugged.net/read/content/' + str(self.message.pk)
        original_text = self.message.content
        return PlainTextContent(original_text + ADD_TEXT)


class MailingList(SendGridClient):
    def send(self, message):
        """
        message -> board.models.Message object
        """
        to_years = message.years.all()
        sendgrid_objects = []
        if to_years.filter(year=0).exists():
            sendgrid_objects = [SendgridMail(message=message, year=0), ]
        else:
            to_years.exclude(year=0)
            sendgrid_objects = [SendgridMail(message=message, year=y.year) for y in to_years]

        # send messages for each year groups
        for sendgrid_object in sendgrid_objects:
            try:
                # send emails here
                response = super().send(sendgrid_object)

                # error handring follows
                x_message_id = response.headers['X-Message-Id']
                requested = True
                error_occurd = False
                error_detail = ''
            except Exception as e:
                x_message_id = ""
                requested = False
                error_occurd = True
                error_detail = e
                # print(e.body)
            finally:
                # save sending logs in MessageProcess
                to_list = [to_emails.email for to_emails in sendgrid_object.to_emails]
                process_list = []
                for email in to_list:
                    obj = MessageProcess(
                        message=message,
                        x_message_id=x_message_id,
                        email=email,
                        Requested=requested,
                        Error_occurd=error_occurd,
                        Error_detail=error_detail,
                        )
                    process_list.append(obj)
                MessageProcess.objects.bulk_create(process_list)

        total_send_num = MessageProcess.objects.filter(message=message, Requested=True, Error_occurd=False).count()
        return total_send_num
