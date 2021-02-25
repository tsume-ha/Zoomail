import datetime
from django.http.response import JsonResponse
from .models import Room

def index(request):
    room = Room()
    now = datetime.datetime.now()
    rooms = {"date": now.strftime("%Y-%m-%d"), "room": room.getByDate(now)}
    return JsonResponse(rooms)

def delete(request):
    room = Room()
    today = datetime.date.today()
    room.deleteByDate(today)
    return JsonResponse({
        'delete': True
    })

def register(request):
    room = Room()
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    room.updateOrCreate('4共24', *[today, tomorrow])
    return JsonResponse({
        'update': True
    })

def sync(request):
    room = Room()
    today = datetime.date.today()
    room.syncFromCalendarToCashe()
    return JsonResponse({
        'sync': True
    })

def get31day(request):
    room = Room()
    contents = room.getByDateRange(
        start_date=datetime.date.today(),
        end_date=datetime.date.today() + datetime.timedelta(days=31)
        )
    return JsonResponse({"rooms": contents})
