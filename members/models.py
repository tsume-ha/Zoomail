from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	google_account = models.EmailField(unique=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	nickname = models.CharField(max_length=255)
	year = models.IntegerField()
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def __str__(self):
		return str(self.id) + self.last_name + self.first_name + self.google_account

