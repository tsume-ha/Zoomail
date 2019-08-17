from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, year=0):
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
            password = password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True) # changed from google_account
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email' # changed from google_account
    REQUIRED_FIELDS = ['year']

    def __str__(self):
        return str(self.id) + self.last_name + self.first_name + self.email # changed from google_account

    def get_short_name(self):
        if self.nickname == "":
            return self.last_name + " " +  self.first_name
        else:
            return self.nickname


