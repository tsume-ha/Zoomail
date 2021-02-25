from django.shortcuts import redirect
from django.urls import reverse

class NewUserRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        form_path = reverse('home:first-register')

        flag = user.is_authenticated\
               and (user.first_name == '' or user.last_name == '' or user.furigana == '')\
               and request.path != form_path
        if flag:
            return redirect(to=form_path)
        