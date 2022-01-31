import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django_ical.views import ICalFeed

from .models import Room


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
    return JsonResponse({
        "room": room,
        "date": today.strftime("%Y-%m-%d")
    })

def getRoomsByRange(start_date, end_date):
    room_list = Room.objects.filter(date__gte=start_date, date__lte=end_date).order_by("date").values("date", "room_name")
    date_list = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    return [{
        "date": date.strftime("%Y-%m-%d"),
        "room": next(
            filter(lambda item: item["date"] == date, room_list),
            {"room_name": None}
        )["room_name"]
    } for date in date_list]

def get31day(request):
    today = datetime.date.today()
    return JsonResponse({
        "rooms": getRoomsByRange(
            start_date = today,
            end_date = today + datetime.timedelta(days=30)
        )
    })