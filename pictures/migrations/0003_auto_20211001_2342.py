# Generated by Django 3.2.6 on 2021-10-01 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pictures.models
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pictures', '0002_auto_20190918_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_album', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='album',
            name='thumbnail',
            field=private_storage.fields.PrivateFileField(blank=True, help_text='JPEGファイルのみ対応しています。<br>5kB以上のファイルをアップロードすると自動的に縮小されます。', null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=pictures.models.custom_upload_to, verbose_name='サムネイル'),
        ),
    ]
