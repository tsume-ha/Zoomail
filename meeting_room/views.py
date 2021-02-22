from django.http.response import JsonResponse
from .models import Room
import datetime


def index(request):
    room = Room()
    now = datetime.datetime.now()
    rooms = {"date": now.strftime("%Y-%m-%d"), "room": room.getByDate(now)}
    return JsonResponse(rooms)

def create(request):
    room = Room()
    now = datetime.datetime.now()
    room.createByDateAPI(now, '4共31')
    # rooms = {"date": now.strftime("%Y-%m-%d"), "room": 'hoge'}
    return JsonResponse({
        'a': True
    })
