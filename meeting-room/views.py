from django.http.response import JsonResponse
from .models import Room
import datetime


def index(request):
    room = Room()
    now = datetime.datetime.now()
    rooms = {"date": now.strftime("%Y-%m-%d"), "room": room.getByDateAPI(now)}
    # if now.hour in range(5):
    #     yesterday = now - datetime.timedelta(days=1)
    #     rooms["date-before"] = yesterday.strftime("%Y-%m-%d")
    #     rooms["room-before"] = room.getByDate(yesterday)

    return JsonResponse(rooms)
