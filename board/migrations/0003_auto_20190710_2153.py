# Generated by Django 2.2.2 on 2019-07-10 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20190709_2320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='sender_id',
            new_name='sender',
        ),
        migrations.RenameField(
            model_name='messages',
            old_name='writer_id',
            new_name='writer',
        ),
        migrations.AlterField(
            model_name='message_year',
            name='mes_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='years', to='board.Messages'),
        ),
    ]
