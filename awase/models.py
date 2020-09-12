from django.db import models
from members.models import User

class Calendar(models.Model):
    title = models.CharField(max_length=64, verbose_name='曲名・バンド名・イベント名')
    text = models.CharField(max_length=400, blank=True, verbose_name='説明')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='calendar_creater')
    days_begin = models.DateField(verbose_name='開始日')
    days_end = models.DateField(verbose_name='終了日')
    invite_key = models.CharField(max_length=32, unique=True, verbose_name='招待用パスワード')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.created_at.strftime('%Y-%m-%d') + ' : ' + self.title

class CalendarUser(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='calendar_content')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_user')
    joined_at = models.DateTimeField(auto_now_add=True)
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
    start_time = models.DateTimeField()
    can_attend = models.NullBooleanField()
    def __str__(self):
        return self.calendar.title


