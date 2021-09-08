# Generated by Django 3.2.6 on 2021-09-05 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0008_delete_kidoku'),
    ]

    operations = [
        migrations.CreateModel(
            name='To',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField()),
                ('text', models.CharField(blank=True, max_length=40, null=True)),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_kaichou', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
