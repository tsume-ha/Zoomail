# Generated by Django 2.2.2 on 2019-06-15 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0002_auto_20190615_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posttest',
            name='post_ID',
        ),
    ]