import datetime
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django_ical.views import ICalFeed

from .models import Room
from .forms import RoomForm


def getRoomsByRange(start_date, end_date):
    room_list = (
        Room.objects.filter(date__gte=start_date, date__lte=end_date).order_by("date").values("date", "room_name")
    )
    date_list = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    return [
        {
            "date": date.strftime("%Y-%m-%d"),
            "room": next(filter(lambda item: item["date"] == date, room_list), {"room_name": None})["room_name"],
        }
        for date in date_list
    ]


class CalendarFeed(ICalFeed):
    """
    A simple event calender
    """

    product_id = "-//ku-unplugged.net//Zoomail_meeting_room_feed//EN"
    timezone = "Asia/Tokyo"
    file_name = "meeting_room.ics"

    def items(self):
        return Room.objects.all().order_by("-date")

    def item_title(self, item):
        return item.room_name

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        return datetime.datetime.combine(item.date, datetime.time())

    def item_link(self, item):
        return "/meeting_room/"


def today(request):
    today = datetime.date.today()
    try:
        room = Room.objects.get(date=today).room_name
    except ObjectDoesNotExist:
        room = None
    return JsonResponse({"room": room, "date": today.strftime("%Y-%m-%d")})


def get31day(request):
    today = datetime.date.today()
    return JsonResponse({"rooms": getRoomsByRange(start_date=today, end_date=today + datetime.timedelta(days=30))})


@login_required()
@permission_required("meeting_room.change_room")
def get_by_month(request):
    if "year" in request.GET:
        year = int(request.GET["year"])
    else:
        year = datetime.date.today().year
    if "month" in request.GET and 1 <= int(request.GET["month"]) <= 12:
        month = int(request.GET["month"])
    else:
        month = int(datetime.date.today().month)
    print(year, month)
    start_date = datetime.date(year=year, month=month, day=1)
    end_date = start_date + relativedelta(months=1) - datetime.timedelta(days=1)
    return JsonResponse({"rooms": getRoomsByRange(start_date=start_date, end_date=end_date)})


@login_required()
@permission_required("meeting_room.change_room")
def register(request):
    if not request.method == "POST":
        return HttpResponse("Bad request", status=400)
    if not "date" in request.POST:
        return HttpResponse("Bad request", status=400)

    date_str = request.POST["date"]
    tdatetime = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)

    try:
        instance = Room.objects.get(date=tdate)
    except ObjectDoesNotExist:
        instance = None

    form = RoomForm(request.POST, instance=instance)
    if form.is_valid():
        content = form.save(commit=False)
        content.updated_at = datetime.datetime.now()
        content.updated_by = request.user
        content.save()
        return JsonResponse({"room": content.room_name, "date": content.date.strftime("%Y-%m-%d")})
    return HttpResponse("Bad request", status=400)
