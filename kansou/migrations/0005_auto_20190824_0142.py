# Generated by Django 2.2.2 on 2019-08-24 01:42

from django.db import migrations, models
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ('kansou', '0004_remove_kansouyoushi_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kansouyoushi',
            name='detail',
            field=models.CharField(blank=True, max_length=200, verbose_name='その他特記事項'),
        ),
        migrations.AlterField(
            model_name='kansouyoushi',
            name='file',
            field=private_storage.fields.PrivateFileField(null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to='kansoyoshi/', verbose_name='PDFファイル'),
        ),
        migrations.AlterField(
            model_name='kansouyoushi',
            name='live',
            field=models.CharField(max_length=200, verbose_name='ライブ名'),
        ),
        migrations.AlterField(
            model_name='kansouyoushi',
            name='numbering',
            field=models.IntegerField(default=1, verbose_name='ナンバリング'),
        ),
        migrations.AlterField(
            model_name='kansouyoushi',
            name='performed_at',
            field=models.DateField(verbose_name='ライブ日'),
        ),
    ]
