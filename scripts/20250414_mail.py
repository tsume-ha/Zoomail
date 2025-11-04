import os
import sys
import json
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

with open("dump.json", "r", encoding="utf-8") as f:
    data = json.load(f)


from mail.models import Message, ToGroup, Attachment

to_group_data = [row for row in data if row["model"] == "board.togroup"]
print(f"Found {len(to_group_data)} to groups in dump.json")
to_groups = []
for row in to_group_data:
    fields = row["fields"]
    to_group = ToGroup(
        pk=row["pk"],
        year=fields["year"],
        leader_id=fields["leader"],
        label=fields["label"],
    )
    to_groups.append(to_group)
print(f"Creating {len(to_groups)} to groups...")
ToGroup.objects.bulk_create(to_groups)
print("To groups created.")

message_data = [row for row in data if row["model"] == "board.message"]
print(f"Found {len(message_data)} messages in dump.json")
messages = []
for row in message_data:
    fields = row["fields"]
    message = Message(
        pk=row["pk"],
        title=fields["title"],
        content=fields["content"],
        sender_id=fields["sender"],
        writer_id=fields["writer"],
        updated_at=datetime.datetime.fromisoformat(fields["updated_at"]),
        created_at=datetime.datetime.fromisoformat(fields["created_at"]),
    )
    messages.append(message)
print(f"Creating {len(messages)} messages...")
Message.objects.bulk_create(messages)
print("Messages created.")

for message in Message.objects.all():
    to_group_data = [
        row
        for row in data
        if row["model"] == "board.messageyear"
        and row["fields"]["message"] == message.pk
    ]
    print(f"Found {len(to_group_data)} to groups for message {message.pk}")
    for row in to_group_data:
        fields = row["fields"]
        to_group = ToGroup.objects.get(year=fields["year"])
        message.to_groups.add(to_group)
print("Messages to groups added.")

from django.core.files.base import ContentFile

message_attachment_data = [row for row in data if row["model"] == "board.attachment"]
print(f"Found {len(message_attachment_data)} message attachments in dump.json")

for row in message_attachment_data:
    fields = row["fields"]
    filepath = os.path.join("private_media", "old", fields["attachment_file"])
    with open(filepath, "rb") as f:
        file_content = f.read()
    content_file = ContentFile(file_content)
    message_attachment = Attachment(
        pk=row["pk"],
        message_id=fields["message"],
        org_filename=os.path.split(fields["attachment_file"])[1],
    )
    message_attachment.file.save(
        os.path.split(fields["attachment_file"])[1], content_file, save=False
    )
    message_attachment.save()
print("Message attachments created.")

for message in Message.objects.filter(attachments__isnull=False):
    for index, attachment in enumerate(message.attachments.all()):
        if index == 0:
            attachment.org_filename = message.title + attachment.extension()
        else:
            attachment.org_filename = (
                message.title + f" ({index})" + attachment.extension()
            )
        attachment.save()
print("Message attachments renamed.")
