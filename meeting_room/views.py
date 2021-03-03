import datetime
import json
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
    content = json.loads(request.body)
    room = Room()
    for key in content:
        dt = datetime.datetime.strptime(content[key]['date'], '%Y-%m-%d')
        room.updateOrCreate(
            content[key]['room'],
            datetime.date(dt.year, dt.month, dt.day)
            )
    return JsonResponse({
        'update': True
    })

def sync(request):
    room = Room()
    room.syncFromCalendarToCashe()
    return get_all(request)

def get31day(request):
    room = Room()
    contents = room.getByDateRange(
        start_date=datetime.date.today(),
        end_date=datetime.date.today() + datetime.timedelta(days=31)
        )
    return JsonResponse({"rooms": contents})

def today(request):
    room = Room()
    return JsonResponse(
        room.getByDate(datetime.date.today())
    )

def get_all(request, page=0):
    """
    page: -1 で前30日
    page: 0で次の30日
    page: 1でその次の30日
    それぞれだいたい1ヶ月ごとにroomsを返す
    """
    room = Room()
    today = datetime.date.today()
    contents = room.getByDateRange(
        start_date=today + datetime.timedelta(days=30 * page),
        end_date=today + datetime.timedelta(days=30 * (page + 1))
        )
    return JsonResponse({"rooms": contents})