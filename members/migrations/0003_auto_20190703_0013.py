# Generated by Django 2.2.2 on 2019-07-03 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20190703_0011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='g_account',
            new_name='google_account',
        ),
    ]
