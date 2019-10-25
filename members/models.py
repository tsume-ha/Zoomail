from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from social_django.models import UserSocialAuth
from django.core import validators
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, email, year=0):
        if not email: # changed from google_account
            raise ValueError('Users must have a Google account')
        user = self.model(
            email = email, # changed from google_account
            year = year,
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, year, password=None): # changed from google_account
        user = self.create_user(
            email, # changed from google_account
            year = year,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        content_social = UserSocialAuth(
            user = user,
            provider = 'google-oauth2',
            uid = email,
            )
        content_social.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Googleアカウント")
    receive_email = models.EmailField(null= True, blank=True, verbose_name="受信用メールアドレス")
    first_name = models.CharField(max_length=255, verbose_name='名前')
    last_name = models.CharField(max_length=255, verbose_name='名字')
    nickname = models.CharField(max_length=255, blank=True, verbose_name='ニックネーム')
    furigana = models.CharField(max_length=255, default="", verbose_name='ふりがな',
                                validators=[RegexValidator(regex=u'^[ぁ-ん]+$',
                                                           message='ふりがなは全角ひらがなのみで入力してください。')])
    year = models.IntegerField(verbose_name='入部年度')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email' # changed from google_account
    REQUIRED_FIELDS = ['year']

    def __str__(self):
        return str(self.year) + ' : ' + self.last_name + self.first_name + '(' + self.email + ')'

    def get_short_name(self):
        if self.nickname == "":
            return self.last_name + self.first_name
        else:
            return self.nickname

    def get_full_name(self):
        return self.last_name + self.first_name

    def get_receive_email(self):
        if self.receive_email == "" or self.receive_email == None:
            return self.email
        else:
            return self.receive_email


class TmpMember(models.Model):
    session = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    furigana = models.CharField(max_length=255)
    year = models.IntegerField(default=0)
    email = models.EmailField()
    def __str__(self):
        return self.session + self.email
