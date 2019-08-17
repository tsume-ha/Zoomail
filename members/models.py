from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, google_account, year, password=None):
        if not google_account:
            raise ValueError('Users must have a Google account')
        user = self.model(
            google_account = google_account,
            year = year,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, google_account, year, password=None):
        user = self.create_user(
            google_account,
            year = year,
            password = password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    google_account = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'google_account'
    REQUIRED_FIELDS = ['year']

    def __str__(self):
        return str(self.id) + self.last_name + self.first_name + self.google_account

    def get_short_name(self):
        if self.nickname == "":
            return self.last_name + " " +  self.first_name
        else:
            return self.nickname


