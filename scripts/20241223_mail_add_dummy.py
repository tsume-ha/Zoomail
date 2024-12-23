import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from members.models import User
from mail.models import Message, ToGroup


# 仮のmessageを作成
user = User.objects.get(id=1)
print(f"Creating message")
message = Message.objects.create(
    title="テストメール",
    content="これはテストメールです。",
    sender=user,
    writer=user,
)
message.to_groups.add(ToGroup.objects.get(year=0))
message.save()
print(f"Created message: {message.title}")
