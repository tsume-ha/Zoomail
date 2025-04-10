import os
import sys
import json
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from members.models import User

with open("dump.json", "r", encoding="utf-8") as f:
    data = json.load(f)


user_data = [row for row in data if row["model"] == "members.user"]
print(f"Found {len(user_data)} users in dump.json")
users = []
for row in user_data:
    fields = row["fields"]
    user = User(
        pk=row["pk"],
        email=fields["email"],
        receive_email=fields["receive_email"],
        livelog_email=fields["livelog_email"],
        send_mail=fields["send_mail"],
        fullname=fields["last_name"] + fields["first_name"],
        nickname=fields["nickname"],
        furigana=fields["furigana"],
        year=fields["year"],
        created_at=datetime.datetime.fromisoformat(fields["created_at"]),
        updated_at=datetime.datetime.fromisoformat(fields["updated_at"]),
        is_staff=fields["is_staff"],
        is_superuser=fields["is_superuser"],
        livelog_login=fields["livelog_login"],
        google_login=fields["google_login"],
    )
    users.append(user)
print(f"Creating {len(users)} users...")
User.objects.bulk_create(users)
print("Users created.")
