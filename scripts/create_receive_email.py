from members.models import User
from mail.models import SendMailAddress

def run():
    contents_list = []
    for user in User.objects.all():
        content = SendMailAddress(
            user = user,
            year = user.year,
            email = user.get_receive_email()
        )
        contents_list.append(content)

    SendMailAddress.objects.bulk_create(contents_list)