from django.shortcuts import redirect
from django.urls import reverse


class FirstRegisterRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        if user.is_authenticated:
            if not user.is_filled_vaild():
                form_path = reverse("members:first_register")
                if request.path != form_path:
                    return redirect(to=form_path)
