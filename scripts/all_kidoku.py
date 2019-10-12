from django.db.models import Q
from members.models import User
from board.models import Message, Kidoku

def run():
    users = User.objects.all()
    for user in users:
        messages_this_user_can_read = Message.objects.filter(Q(years__year=user.year) | Q(years__year=0))
        for message in messages_this_user_can_read:
            if not Kidoku.objects.filter(message=message).filter(user=user).exists():
                content = Kidoku(message=message, user=user, have_read=True)
                content.save()
            else:
                content = Kidoku.objects.filter(message=message).get(user=user)
                content.have_read = True
                content.save()