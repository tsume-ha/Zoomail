from django.contrib.messages import get_messages

class AjaxMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
            return response
        
        storage = get_messages(request)# ここでmessageは削除される
        for message in storage:
            # response.set_cookie(message.tags, message.message)
            print(message.tags)
            print(message.message)

        return response

