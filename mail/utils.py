from .models import Message, Attachment
from members.models import User


def can_read_message(message: Message, user: User) -> bool:
    years = message.to_groups.all().values_list("year", flat=True)
    if 0 in years:
        return True
    if user.year in years:
        return True
    if message.sender == user:
        return True
    if message.writer == user:
        return True
    return False
