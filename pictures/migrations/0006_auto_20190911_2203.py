# Generated by Django 2.2.2 on 2019-09-11 22:03

from django.db import migrations
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0005_remove_album_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='thumbnail',
            field=private_storage.fields.PrivateFileField(null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to='album_one_image/%Y', verbose_name='サムネイル'),
        ),
    ]
