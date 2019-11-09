from django.db.models import Q
from members.models import User
from board.models import Message, Kidoku

def run():
    users = User.objects.all()
    for user in users:
        messages_this_user_can_read = Message.objects.filter(Q(years__year=user.year) | Q(years__year=0))
        for message in messages_this_user_can_read:
            c = Kidoku.objects.get_or_create(message=message, user=user, have_read=True)