# Generated by Django 2.2.2 on 2019-10-25 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='receive_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='受信用メールアドレス'),
        ),
    ]
