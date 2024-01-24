from enum import Enum

import pandas as pd

from board.models import Message
from mail.models import SendMailAddress, MailLog
from django.conf import settings
from .sendgrid import SendGridClient, SendgridMail
from .ses import build_raw_mail, SESSender

AWS_SES_SEND_NUM = settings.AWS_SES_SEND_NUM
AWS_SES_SEND_RATE = 10


class MailStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class SendServers(Enum):
    SENDGRID = "sendgrid"
    SES = "ses"


class MailisSender:
    def __init__(self, message: Message):
        self.message = message
        self.subject = message.title
        self.text_content = message.content
        self.attachments = message.attachments.all()
        self.from_name = message.writer.get_short_name()
        self.to_emails_df: pd.DataFrame = self.compose_to_emails(message)
        self.to_emails_df["send_serer"] = None
        self.to_emails_df["status"] = MailStatus.PENDING
        self.to_emails_df["mail_id"] = None
        self.to_emails_df["error"] = None
        self.to_emails_df = self.assign_send_server(self.to_emails_df)

    def compose_to_emails(self, message) -> pd.DataFrame:
        if message.years.filter(year=0).exists():
            addresses = SendMailAddress.objects.all().values_list("email", "user", flat=False)
            df = pd.DataFrame(addresses, columns=["email", "user"])
            df["from_email"] = "zenkai@zoomail.ku-unplugged.net"
            df["allow_sendgrid"] = True
            df["allow_ses"] = True
        else:
            df_list = []
            for group in message.years.all():
                addresses = SendMailAddress.objects.filter(user__year=group.year).values_list(
                    "email", "user", flat=False
                )
                df_group = pd.DataFrame(addresses, columns=["email", "user"])
                df_group["from_email"] = f"{group.year - 1994}kaisei@zoomail.ku-unplugged.net"
                df_list.append(df_group)
            df = pd.concat(df_list, axis=0)
            df = df.drop_duplicates(subset=["user"])
            df["allow_sendgrid"] = True
            df["allow_ses"] = True
        return df

    def assign_send_server(self, df: pd.DataFrame) -> pd.DataFrame:
        allow_ses_df = df[df["allow_ses"]]
        print(df)
        df.loc[allow_ses_df.sample(n=self.get_ses_num()).index, "send_server"] = SendServers.SES
        df.loc[df["send_server"].isnull(), "send_server"] = SendServers.SENDGRID
        print(df)
        return df

    def get_ses_num(self):
        if len(self.to_emails_df) < AWS_SES_SEND_NUM:
            return len(self.to_emails_df)
        else:
            return AWS_SES_SEND_NUM

    def send(self):
        self.send_by_sendgrid()
        self.send_by_ses()
        return len(self.to_emails_df)

    def send_by_sendgrid(self):
        sendgrid_df = self.to_emails_df[self.to_emails_df["send_server"] == SendServers.SENDGRID]
        for from_email, group_df in sendgrid_df.groupby(["from_email"]):
            client = SendGridClient()
            mail = SendgridMail(
                from_email=from_email,
                to_emails=group_df["email"].tolist(),
                subject=self.subject,
                plain_text_content=self.text_content,
                is_multiple=True,
                reply_to=None,
                html_content=None,
                amp_html_content=None,
                global_substitutions=None,
                attachments=self.attachments,
            )
            try:
                response = client.send(mail)
                x_message_id = response.headers["X-Message-Id"]
                group_df["mail_id"] = x_message_id
                group_df["status"] = MailStatus.SUCCESS
            except Exception as e:
                group_df["status"] = MailStatus.FAILED
                group_df["mail_id"] = ""
                group_df["error"] = str(e)

        log_list = []
        for index, row in sendgrid_df.iterrows():
            log = MailLog(
                message=self.message,
                mail_id=row["mail_id"],
                email=row["email"],
                user_id=row["user"],
                send_server=MailLog.SendServerChoices.SENDGRID,
                status=row["status"],
                error=row["error"],
            )
            log_list.append(log)
        MailLog.objects.bulk_create(log_list)

    def send_by_ses(self):
        ses_df = self.to_emails_df[self.to_emails_df["send_server"] == SendServers.SES]
        # ses_dfを10行ずつ分割してfor文で回す
        for i in range(len(ses_df) // AWS_SES_SEND_RATE + 1):
            group_df = ses_df[AWS_SES_SEND_RATE * i : min(AWS_SES_SEND_RATE * (i + 1), len(ses_df))]
            log_list = []
            for index, row in group_df.iterrows():
                mail = build_raw_mail(
                    from_email=row["from_email"],
                    from_name=self.from_name,
                    to_emails=[row["email"]],
                    subject=self.subject,
                    text_content=self.text_content,
                    html_content=None,
                    attachments=self.attachments,
                )
                client = SESSender()
                try:
                    response = client.send(mail)
                    mail_id = response["MessageId"]
                    row["mail_id"] = mail_id
                    row["status"] = MailStatus.SUCCESS
                except Exception as e:
                    row["status"] = MailStatus.FAILED
                    row["mail_id"] = ""
                    row["error"] = str(e)
                finally:
                    log = MailLog(
                        message=self.message,
                        mail_id=row["mail_id"],
                        email=row["email"],
                        user_id=row["user"],
                        send_server=MailLog.SendServerChoices.SES,
                        status=row["status"],
                        error=row["error"],
                    )
                    log_list.append(log)

            MailLog.objects.bulk_create(log_list)
