from django.db import models
from django.utils import timezone
from members.models import User

class Message(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()

	#添付ファイルの有無
	attachment = models.BooleanField(default=False)
	sender_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='send_message')
	# sender_id = models.IntegerField()

	#転載時に使用。
	#文章を書いた人がwriter、アップロードした人がsender。
	#通常なら sender == writer で同じになる。
	writer_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='write_message')	
	# writer_id = models.IntegerField()
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	
	def __str__(self):
		return 'mes_ID=' + str(self.id) + ', title=' + self.title
		
class Year(models.Model):
	messages = models.ManyToManyField(Message)
	year = models.IntegerField()

	ALL = -1
	def display(self):
		if self.year == self.ALL:
			return "ALL"
		
		return self.year


	def __str__(self):
		return self.display()

class Attachment(models.Model):
	message = models.ForeignKey(Message, null=True, on_delete=models.CASCADE)
	attachment = models.FileField()
	def __str__(self):
		return self.message.title

class Tag(models.Model):
	name = models.CharField(max_length=30)
	messages = models.ManyToManyField(Message)
	def __str__(self):
		return self.name
