from enum import Enum
import time
import datetime

import pandas as pd

from board.models import Message
from mail.models import SendMailAddress, MailLog
from django.conf import settings
from .sendgrid import SendGridClient, SendgridMail
from .ses import build_raw_mail, SESSender

SENDGRID_SEND_NUM = settings.SENDGRID_SEND_NUM
AWS_SES_SEND_NUM = settings.AWS_SES_SEND_NUM
AWS_SES_SEND_RATE = settings.AWS_SES_SEND_RATE
EMAIL_USE_SENDGRID = settings.EMAIL_USE_SENDGRID
EMAIL_USE_SES = settings.EMAIL_USE_SES


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
        self.text_content = (
            message.content + "\n\n--------------------------------"
            "\nこのメーリスのURLはこちら\nhttps://zoomail.ku-unplugged.net/mail/" + str(self.message.pk)
        )
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
        if EMAIL_USE_SENDGRID and not EMAIL_USE_SES:
            df["send_server"] = SendServers.SENDGRID
        elif not EMAIL_USE_SENDGRID and EMAIL_USE_SES:
            df["send_server"] = SendServers.SES
        elif EMAIL_USE_SENDGRID and EMAIL_USE_SES:
            df.loc[df.sample(n=self.get_sendgrid_num()).index, "send_server"] = SendServers.SENDGRID
            df.loc[df["send_server"].isnull(), "send_server"] = SendServers.SES
        return df

    def get_ses_num(self):
        """
        Amazon SESを利用して送信する件数を指定する
        """
        # 今月のSendgridで送信したメールの件数
        today = datetime.date.today()
        this_month_start = datetime.date.today().replace(day=1)
        sendgrid_logs = MailLog.objects.filter(
            send_server=MailLog.SendServerChoices.SENDGRID,
            created_at__range=(this_month_start, today),
            status=MailStatus.SUCCESS,
        )
        sendgrid_num = sendgrid_logs.count()
        # print("Sendgrid mails count this month: ", sendgrid_num)

        if sendgrid_num < 10000:
            return min(len(self.to_emails_df), AWS_SES_SEND_NUM)

        ratio = min(1, (sendgrid_num - 10000) / 2000)
        return min(len(self.to_emails_df), int(AWS_SES_SEND_NUM * ratio))

    def get_sendgrid_num(self):
        """
        sendgridを利用して送信する件数を指定する
        過去24hに100件まで送る。
        """
        now = datetime.datetime.now()
        sendgrid_logs = MailLog.objects.filter(
            send_server=MailLog.SendServerChoices.SENDGRID,
            created_at__range=(now - datetime.timedelta(hours=24), now),
            status=MailStatus.SUCCESS,
        )
        sendgrid_num = sendgrid_logs.count()
        if sendgrid_num >= 100:
            return 0
        else:
            return min(len(self.to_emails_df), SENDGRID_SEND_NUM - sendgrid_num)

    def send(self):
        if EMAIL_USE_SENDGRID:
            self.send_by_sendgrid()
        if EMAIL_USE_SES:
            self.send_by_ses()
        return len(self.to_emails_df)

    def send_by_sendgrid(self):
        sendgrid_df = self.to_emails_df[self.to_emails_df["send_server"] == SendServers.SENDGRID]
        for from_email, group_df in sendgrid_df.groupby(["from_email"]):
            client = SendGridClient()
            mail = SendgridMail(
                from_email=(from_email, self.from_name),
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
                sendgrid_df.loc[group_df.index, "mail_id"] = x_message_id
                sendgrid_df.loc[group_df.index, "status"] = MailStatus.SUCCESS.value
            except Exception as e:
                sendgrid_df.loc[group_df.index, "status"] = MailStatus.FAILED.value
                sendgrid_df.loc[group_df.index, "mail_id"] = ""
                sendgrid_df.loc[group_df.index, "error"] = str(e)

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
            if i > 0:
                time.sleep(1)
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
                    row["status"] = MailStatus.SUCCESS.value
                except Exception as e:
                    row["status"] = MailStatus.FAILED.value
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
