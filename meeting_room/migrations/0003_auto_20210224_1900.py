# Generated by Django 2.2.4 on 2021-02-24 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_room', '0002_cashe_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashe',
            name='event_id',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cashe',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
