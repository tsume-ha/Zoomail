# Generated by Django 4.2.10 on 2024-06-09 23:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Emailアドレス')),
                ('receive_email', models.EmailField(blank=True, max_length=254, verbose_name='受信用メールアドレス')),
                ('livelog_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Livelogメールアドレス')),
                ('send_mail', models.BooleanField(default=True, verbose_name='メーリスを受信する')),
                ('fullname', models.CharField(max_length=255, verbose_name='フルネーム')),
                ('nickname', models.CharField(blank=True, max_length=255, verbose_name='ニックネーム')),
                ('furigana', models.CharField(default='', max_length=255, validators=[django.core.validators.RegexValidator(message='ふりがなは全角ひらがなのみで入力してください。', regex='^[ぁ-んー]+$')], verbose_name='ふりがな')),
                ('year', models.IntegerField(help_text='2024年4月入部の場合、2024を入力してください。', verbose_name='入部年度')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('livelog_login', models.BooleanField(default=False)),
                ('google_login', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestMail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='送信したメールアドレス')),
                ('sent_at', models.DateTimeField()),
                ('x_message_id', models.CharField(editable=False, max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_mail', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]