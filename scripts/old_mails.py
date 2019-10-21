from config.settings import BASE_DIR
import os
import eml_parser
from board.models import Message

def run():
    target = os.path.join(BASE_DIR, 'scripts', 'emails', '2917.eml')
    print(target)
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
        print(from_mail_address)
        print(send_at)
        print(message_title)
        print(message_content)

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