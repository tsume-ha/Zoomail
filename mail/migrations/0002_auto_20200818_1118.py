# Generated by Django 2.2.4 on 2020-08-18 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageprocess',
            name='Error_detail',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='エラー詳細'),
        ),
        migrations.AlterField(
            model_name='messageprocess',
            name='x_message_id',
            field=models.CharField(blank=True, editable=False, max_length=100, null=True),
        ),
    ]
