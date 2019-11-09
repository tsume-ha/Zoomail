from config.settings import BASE_DIR
import os
import eml_parser
import datetime
from board.models import Message, MessageYear, Kidoku
from members.models import User

def run():
    admin = User.objects.get(email='developer@ku-unplugged.net')
    for i in range(2800,2870):
        name = str(i) + '.eml'
        target = os.path.join(BASE_DIR, 'scripts', 'emails', name)
        try:
            with open(target, 'rb') as file:
                raw_email = file.read()
                parsed_eml = eml_parser.eml_parser.decode_email_b(
                    eml_file = raw_email,
                    include_raw_body = True,
                    )
                from_mail_address = parsed_eml['header']['from']
                send_at = parsed_eml['header']['date']
                message_title = parsed_eml['header']['header']['subject'][0]
                message_content = parsed_eml['body'][0]['content']
                send_at = datetime.datetime(
                    send_at.year,
                    send_at.month,
                    send_at.day,
                    send_at.hour,
                    send_at.minute,
                    send_at.second)
                send_at = send_at + datetime.timedelta(hours=9)
                content = Message(
                    title = message_title,
                    content = message_content,
                    updated_at = send_at,
                    created_at = send_at,
                    sender = admin,
                    writer = admin
                    )
                content.save()
                content_year = MessageYear(
                    message = content,
                    year = 0)
                content_year.save()

                for user in User.objects.all():
                    Kidoku.objects.get_or_create(message=content, user=user)
                print(i)
        except FileNotFoundError:
            continue
    

# {'body': [
#     {'content_header': {'content-type': ['text/plain; charset="iso-2022-jp"']},
#      'content_type': 'text/plain', 
#      'hash': 'f6a1239f143ccf6f60803ef4e61576399e10f1ca4e4f1e827bb62f875210ae6d'}],
# 'header': {'subject': '[k-u-unplugged:2917] 5 月度会計報告', 
#            'from': 'goto1227_r@yahoo.co.jp',
#            'to': ['k-u-unplugged@freeml.com'],
#            'date': datetime.datetime(2019, 6, 2, 9, 15, 45, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))),
#            'received': [],
#            'header': {'x-mlccount': ['2917'],
#                       'date': ['Sun, 02 Jun 2019 09:15:45 +0900'],
#                       'x-mailer': ['freeml (https://www.freeml.com/)'],
#                       'content-type': ['text/plain; charset="iso-2022-jp"'],
#                       'to': ['k-u-unplugged@freeml.com'],
#                       'message-id': ['<VAHG5enziN2zw61xQJWqYG5vJPMgYrv6HPYIv04BA@prod-freeml-batch01.local.freeml.com>'],
#                       'from': ['goto1227_r@yahoo.co.jp'],
#                       'mime-version': ['1.0'],
#                       'subject': ['[k-u-unplugged:2917] 5月度会計報告']}
#                }
# }