import datetime
import json
from dateutil.relativedelta import relativedelta
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required

from config.permissions import MeetingroomPermission
from .models import Room

@login_required()
def index(request):
    # return permission
    return JsonResponse({
        "meeting_room_permission": MeetingroomPermission(request.user)
    })

@login_required()
def register(request):
    if not MeetingroomPermission(request.user):
        return JsonResponse({
            "results": "403 Forbidden"
        })
    content = json.loads(request.body)
    room = Room()
    results = []
    for key in content:
        dt = datetime.datetime.strptime(content[key]['date'], '%Y-%m-%d')
        result = room.updateOrCreate(
            content[key]['room'],
            datetime.date(dt.year, dt.month, dt.day)
            )
        results.append({key: result})
    return JsonResponse({
        "results": results
    })

@login_required()
def sync(request):
    if not MeetingroomPermission(request.user):
        return JsonResponse({
            "results": "403 Forbidden"
        })
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

@login_required()
def get_all(request):
    """
    page: -1 で先月
    page: 0で今月
    page: 1で来月
    といった風に1ヶ月ごとにroomsを返す
    """
    if not MeetingroomPermission(request.user):
        return JsonResponse({
            "results": "403 Forbidden"
        })
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
    