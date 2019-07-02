from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
	def create_superuser(self, google_account, password=None):
		user = self.create_user(
			google_account,
			password=password,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser, PermissionsMixin):
	google_account = models.EmailField(unique=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	nickname = models.CharField(max_length=255)
	year = models.IntegerField()
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

	USERNAME_FIELD = 'google_account'
	REQUIRED_FIELDS = []

	def __str__(self):
		return str(self.id) + self.last_name + self.first_name + self.google_account

