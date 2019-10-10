# Generated by Django 2.2.2 on 2019-10-11 01:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('awase', '0005_auto_20191011_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='days_begin',
            field=models.DateField(default=datetime.datetime(2019, 10, 11, 1, 7, 6, 118998)),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='days_end',
            field=models.DateField(default=datetime.datetime(2020, 1, 19, 1, 7, 6, 118998)),
        ),
        migrations.AlterField(
            model_name='calendaruser',
            name='calender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendar_content', to='awase.Calendar'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='calender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendar_schedule', to='awase.Calendar'),
        ),
    ]