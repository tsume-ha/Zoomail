# Generated by Django 2.2.2 on 2019-06-15 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_ID', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('content', models.CharField(max_length=100000)),
                ('created_at', models.DateTimeField()),
                ('whosend', models.IntegerField()),
                ('whopost', models.IntegerField()),
            ],
        ),
    ]
