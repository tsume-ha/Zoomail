from django.db import models
from members.models import User

class SpecialPage(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    key = models.CharField(max_length=64)
    html_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title + ' ' + self.html_name

def ContentLog():
    from kansou.models import Kansouyoushi
    from movie.models import YoutubeURL
    from pictures.models import Album
    from player.models import Performance

    LIST_NUM = 3

    kansou_list = [('kansou', q.created_at, q.live) for q in Kansouyoushi.objects.order_by('-created_at')[:LIST_NUM]]
    movie_list = [('movie', q.created_at, q.title) for q in YoutubeURL.objects.order_by('-created_at')[:LIST_NUM]]
    pictures_list = [('pictures', q.created_at, q.title) for q in Album.objects.order_by('-created_at')[:LIST_NUM]]
    player_list = [('player', q.updated_at, q.live_name) for q in Performance.objects.order_by('-updated_at')[:LIST_NUM]]

    log_list = kansou_list + movie_list + pictures_list + player_list
    log_list.sort(key=lambda tup: tup[1], reverse=True)

    return log_list[:LIST_NUM]