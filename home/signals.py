from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import NewContent

from kansou.models import Kansouyoushi
from movie.models import YoutubeURL
from pictures.models import Album
from sound.models import Live

LIST_NUM = 5

@receiver(post_save, sender=Kansouyoushi)
@receiver(post_save, sender=YoutubeURL)
@receiver(post_save, sender=Album)
@receiver(post_save, sender=Live)
def update_send_mail_address(sender, instance, **kwargs):
    kansou_list = [{
        'genre': '感想用紙',
        'title': q.title,
        'date': q.created_at,
        'path': '/kansou/'
    } for q in Kansouyoushi.objects.order_by('-created_at')[:LIST_NUM]]
    movie_list = [{
        'genre': 'ライブ映像',
        'title': q.title,
        'date': q.created_at,
        'path': '/movie/'
    } for q in YoutubeURL.objects.order_by('-created_at')[:LIST_NUM]]
    pictures_list = [{
        'genre': '写真',
        'title': q.title,
        'date': q.created_at,
        'path': '/pictures/'
    } for q in Album.objects.order_by('-created_at')[:LIST_NUM]]
    sound_list = [{
        'genre': 'リハ音源',
        'title': q.live_name,
        'date': q.created_at,
        'path': '/sound/{}/'.format(q.pk)
    } for q in Live.objects.order_by('-updated_at')[:LIST_NUM]]

    log_list = kansou_list + movie_list + pictures_list + sound_list
    log_list.sort(key=lambda obj: obj['date'], reverse=True)
    for i in range(min(LIST_NUM - 1, len(log_list))):
        NewContent.objects.update_or_create(
            index = i,
            defaults={
                'genre': log_list[i]['genre'],
                'title': log_list[i]['title'],
                'path': log_list[i]['path'],
                'date': log_list[i]['date'],
            }
        )
