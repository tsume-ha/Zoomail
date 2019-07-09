from django.db import models
from django.utils import timezone
from members.models import User

class Messages(models.Model):
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
		
class Message_Year(models.Model):
	mes_ID = models.ForeignKey('Messages', null=True, on_delete=models.CASCADE)
	year = models.IntegerField()
	def __str__(self):
		return self.mes_ID.title + str(self.year)

class Message_Attachment(models.Model):
	mes_ID = models.ForeignKey('Messages', null=True, on_delete=models.CASCADE)
	attachment = models.FileField()
	def __str__(self):
		return self.mes_ID.title

class Message_Tag(models.Model):
	mes_ID = models.ForeignKey('Messages', null=True, on_delete=models.CASCADE)
	tag = models.CharField(max_length=30)
	def __str__(self):
		return self.mes_ID.title + self.tag