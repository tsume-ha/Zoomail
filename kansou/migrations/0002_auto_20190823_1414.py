# Generated by Django 2.2.2 on 2019-08-23 14:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kansou', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Attachment',
            new_name='Kansouyoushi',
        ),
    ]
