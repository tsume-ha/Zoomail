from googleapiclient.discovery import build
from django.conf import settings


def createService():
    return build("calendar", "v3", developerKey=settings.GOOGLE_CALENDAR_API_KEY)
