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
    today = datetime.date.today()
    room.createByDateAPI(today, '4共21')
    return JsonResponse({
        'a': True
    })
