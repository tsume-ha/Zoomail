# Generated by Django 2.2.2 on 2020-03-01 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20191128_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='send_mail',
            field=models.BooleanField(default=True),
        ),
    ]
