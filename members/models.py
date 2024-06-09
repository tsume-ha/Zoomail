from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator

from social_django.models import UserSocialAuth


class UserManager(BaseUserManager):
    def create_user(self, email, year=0):
        if not email:
            raise ValueError("Users must have a email address")
        user = self.model(
            email=email,
            year=year,
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, year, password=None):
        user = self.create_user(
            email,
            year=year,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        content_social = UserSocialAuth(
            user=user,
            provider="google-oauth2",
            uid=email,
        )
        content_social.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Emailアドレス")
    receive_email = models.EmailField(
        blank=True, null=False, verbose_name="受信用メールアドレス"
    )
    livelog_email = models.EmailField(
        blank=True, null=True, verbose_name="Livelogメールアドレス"
    )
    send_mail = models.BooleanField(default=True, verbose_name="メーリスを受信する")
    fullname = models.CharField(max_length=255, verbose_name="フルネーム")
    nickname = models.CharField(max_length=255, blank=True, verbose_name="ニックネーム")
    furigana = models.CharField(
        max_length=255,
        default="",
        verbose_name="ふりがな",
        validators=[
            RegexValidator(
                regex="^[ぁ-んー]+$",
                message="ふりがなは全角ひらがなのみで入力してください。",
            )
        ],
    )
    year = models.IntegerField(
        verbose_name="入部年度",
        help_text="2024年4月入部の場合、2024を入力してください。",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    livelog_login = models.BooleanField(default=False)
    google_login = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["year"]

    def __str__(self):
        return str(self.year) + " " + self.fullname

    def set_password(self, *args, **kwargs):
        raise ValidationError("Password can not be set!")

    def get_short_name(self):
        if self.nickname == "":
            return self.fullname
        else:
            return self.nickname

    def get_receive_email(self):
        if self.receive_email == "" or self.receive_email is None:
            return self.email
        else:
            return self.receive_email


class TestMail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_mail")
    email = models.EmailField(verbose_name="送信したメールアドレス")
    sent_at = models.DateTimeField()
    x_message_id = models.CharField(max_length=100, editable=False)

    def __str__(self):
        return self.user.fullname + " - " + self.email
