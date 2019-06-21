from django.db import models

class PostTest(models.Model):
	"""docstring for PostTest"""
	title = models.CharField(max_length=200)
	content = models.TextField()
	created_at = models.DateTimeField()
	whosend = models.IntegerField()
	whopost = models.IntegerField()

	def __str__(self):
		return 'post_ID=' + str(self.id) + ', title=' + self.title


class Messages(object):
	"""docstring for Messages"""
	title = models.CharField(max_length=200)
	content = models.TextField()
	attachment = models.BooleanField(defalt=False)
		#添付ファイル
	sender_id = IntegerField()
	writer_id = IntegerField()
		#転載時に使用。
		#文章を書いた人がwriter、アップロードした人がsender。
		#通常なら sender == writer で同じになる。
	created_at = DateTimeField()
	updated_at = DateTimeField()
	def __init__(self):
		return 'mes_ID=' + str(self.id) + ', title=' + self.title
		