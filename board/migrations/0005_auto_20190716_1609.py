# Generated by Django 2.2.2 on 2019-07-16 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_remove_message_all'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='attachment',
            field=models.FileField(null=True, upload_to='document/%Y/%m/%d'),
        ),
    ]