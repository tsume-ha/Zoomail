# Generated by Django 2.2.2 on 2019-09-16 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubeurl',
            name='textcontent',
            field=models.TextField(blank=True, max_length=2000, verbose_name='テキスト'),
        ),
    ]