# Generated by Django 3.2.6 on 2021-11-21 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kansou', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kansouyoushi',
            old_name='live',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='kansouyoushi',
            name='numbering',
        ),
    ]