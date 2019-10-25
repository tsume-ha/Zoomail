from django.db import models
from members.models import User

class SpecialPage(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    key = models.CharField(max_length=64)
    html_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title + ' ' + self.html_name