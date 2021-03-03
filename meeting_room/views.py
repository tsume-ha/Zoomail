import datetime
import json
from dateutil.relativedelta import relativedelta
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

def get_all(request):
    """
    page: -1 で先月
    page: 0で今月
    page: 1で来月
    といった風に1ヶ月ごとにroomsを返す
    """
    page = 0
    if 'page' in request.GET:
        page = int(request.GET['page'])
    room = Room()
    today = datetime.date.today()
    start = today.replace(day=1) + relativedelta(months=page)
    end = today.replace(day=1) + relativedelta(months=page+1) - datetime.timedelta(days=1)
    contents = room.getByDateRange(
        start_date=start, end_date=end
        )
    return JsonResponse({"rooms": contents})
    