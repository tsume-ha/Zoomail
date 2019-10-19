from django.db import models
from members.models import User
import datetime

class Calendar(models.Model):
    title = models.CharField(max_length=200, verbose_name='曲名・バンド名・イベント名')
    text = models.CharField(max_length=400, blank=True, verbose_name='説明')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='calendar_creater')
    days_begin = models.DateField(default=datetime.date.today(), verbose_name='開始日')
    days_end = models.DateField(default=datetime.date.today()+datetime.timedelta(days=60), verbose_name='終了日')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.created_at.strftime('%Y-%m-%d') + self.title

class CalendarUser(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='calendar_content')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_user')
    def __str__(self):
        return self.calendar.title + ' : ' + self.user.get_full_name()

class CollectHour(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='calendar_hour')
    date = models.DateField(verbose_name='日付')
    hour_begin = models.PositiveSmallIntegerField(default=9, null=False, verbose_name='開始時間')
    hour_end = models.PositiveSmallIntegerField(default=26, null=False, verbose_name='終了時間')
    def __str__(self):
        return self.calendar.title + ' : ' + self.date.strftime('%Y-%m-%d') + ' ' + str(self.hour_begin) + '-' + str(self.hour_end)


class Schedule(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='calendar_schedule')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule_user')
    date = models.DateField(null=False)
    starttime = models.PositiveSmallIntegerField(null=False)
    duration = models.IntegerField(default=30)
    canattend = models.BooleanField()
    def __str__(self):
        return self.calendar.title + ' ' + self.user.get_full_name + self.starttime.strftime(' %Y-%m-%d %H:%M') + ' ' + self.canattend


