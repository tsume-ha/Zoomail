# Generated by Django 3.2.6 on 2021-09-09 13:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0009_to'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='To',
            new_name='ToGroup',
        ),
    ]