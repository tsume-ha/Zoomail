import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from members.models import User
from mail.models import Message, ToGroup


# 仮のユーザーを作成
init_user_email = os.environ.get("INIT_USER_EMAIL", "example@ku-unplugged.net")
print(f"Creating user: {init_user_email}")
init_user = User.objects.create_superuser(
    email=init_user_email,
    year=2024,
)
init_user.fullname = "管理者アカウント"
init_user.nickname = "管理者"
init_user.save()
print(f"Created user: {init_user.email}")

# 作成したユーザを会長にして、ToGroupを作成
print("Creating ToGroup")
to_group = ToGroup.objects.create(year=0, leader=None, label="全回メーリス")
print(f"Created ToGroup: {to_group.text()}")
to_group = ToGroup.objects.create(year=2024, leader=init_user)
print(f"Created ToGroup: {to_group.text()}")
