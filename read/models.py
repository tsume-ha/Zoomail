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
		