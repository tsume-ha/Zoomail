# Generated by Django 2.2.4 on 2020-09-13 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awase', '0002_auto_20200229_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='title',
            field=models.CharField(max_length=64, verbose_name='曲名・バンド名・イベント名'),
        ),
    ]
