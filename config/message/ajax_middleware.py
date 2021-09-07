import time
from urllib.parse import quote
from django.contrib.messages import get_messages

class AjaxMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
            return response

        i = 0
        now = int(time.time())
        storage = get_messages(request)# ここでmessageは削除される
        for message in storage:
            response.set_cookie("message_{:010}_{:02}_{}".format(now, i, message.tags), quote(message.message, safe='~'))
            i += 1

        return response

