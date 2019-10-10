from django.db import models
from members.models import User
import datetime

class Calendar(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    text = models.CharField(max_length=400, blank=True, verbose_name='Description')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='calendar_creater')
    days_begin = models.DateField(default=datetime.date.today())
    days_end = models.DateField(default=datetime.date.today()+datetime.timedelta(days=60))
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.created_at.strftime('%Y-%m-%d') + self.title

class CalendarUser(models.Model):
    calender = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='calendar_content')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_user')
    def __str__(self):
        return self.calender.title + ' : ' + self.user.get_full_name()

class Schedule(models.Model):
    calender = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='calendar_schedule')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule_user')
    starttime = models.DateTimeField()
    duration = models.IntegerField(default=30)
    canattend = models.BooleanField()
    def __str__(self):
        return self.calender.title + ' ' + self.user.get_full_name + self.starttime.strftime(' %Y-%m-%d %H:%M') + ' ' + self.canattend


