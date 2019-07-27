from django.db import models
from django.utils import timezone
from members.models import User
from private_storage.fields import PrivateFileField

class Performance(models.Model):
	live_name = models.CharField(max_length=255)
	song_num = models.IntegerField()
	recorded_at = models.DateField()
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='perform_updated_by')
	def __str__(self):
		return str(self.id) + self.live_name

class Song(models.Model):
	performance = models.ForeignKey(Performance, on_delete=models.CASCADE)	
	track_num = models.IntegerField()
	song_name = models.CharField(max_length=500)
	file = PrivateFileField(upload_to='music/%Y/%m/%d', null=True)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='song_updated_by')
	def __str__(self):
		return str(self.track_num) + self.song_name