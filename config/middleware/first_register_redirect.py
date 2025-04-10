from django.shortcuts import redirect
from django.urls import reverse


class FirstRegisterRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            if not user.is_filled_vaild():
                form_path = reverse("members:first_register")
                auth_path = "/auth/"
                if request.path != form_path and not str(request.path).startswith(
                    auth_path
                ):
                    return redirect(form_path)

        response = self.get_response(request)
        return response
