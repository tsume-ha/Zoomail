# Generated by Django 2.2.2 on 2019-11-07 22:24

import board.models
from django.db import migrations
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_auto_20191021_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='attachment',
        ),
        migrations.AlterField(
            model_name='attachment',
            name='attachment_file',
            field=private_storage.fields.PrivateFileField(blank=True, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=board.models.custom_upload_to),
        ),
    ]
