# Generated by Django 3.2.6 on 2022-01-12 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sound', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='live',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='sound.live'),
        ),
    ]
