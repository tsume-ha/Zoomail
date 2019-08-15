import os
from django.db import models
from django.utils import timezone
from members.models import User
from private_storage.fields import PrivateFileField

class Message(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()

	#添付ファイルの有無
	attachment = models.BooleanField(default=False)
	sender_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='send_message')

	#転載時に使用。
	#文章を書いた人がwriter、アップロードした人がsender。
	#通常なら sender == writer で同じになる。
	writer_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='write_message')	

	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	
	def __str__(self):
		return 'mes_ID=' + str(self.id) + ', title=' + self.title
		
class MessageYear(models.Model):
	year = models.IntegerField()
	message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='years')

	ALL = -1

	def display(self):
		if self.year == self.ALL:
			return "全回"
		
		return self.year

class Attachment(models.Model):
	message = models.ForeignKey(Message, null=True, on_delete=models.CASCADE, related_name='attachments')
	attachment_file = PrivateFileField(upload_to='document/%Y/%m/%d', null=True)
	def __str__(self):
		return self.message.title
	
	def extension(self):
		_, extension = os.path.splitext(self.attachment_file.name)
		return extension

	def isImage(self):
		return self.extension() in [".gif", ".png", ".jpeg", ".jpg", ".bmp", ".GIF", ".PNG", ".JPEG", ".JPG", ".BMP"]

	def fileName(self):
		_, fileName = os.path.split(self.attachment_file.name)
		return fileName

class Tag(models.Model):
	name = models.CharField(max_length=30)
	messages = models.ManyToManyField(Message)
	def __str__(self):
		return self.name
