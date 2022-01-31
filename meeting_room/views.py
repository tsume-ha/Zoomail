import datetime

from django_ical.views import ICalFeed

from .models import Room


class EventFeed(ICalFeed):
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
