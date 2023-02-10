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
        form_path = reverse("first-register")
        user_fetch_path = reverse("api:tempuser")
        first_register_api_path = reverse("api:first_register_api")

        if user.is_authenticated:
            if user.first_name == "" or user.last_name == "" or user.furigana == "":
                if (
                    request.path != form_path
                    and request.path != user_fetch_path
                    and request.path != first_register_api_path
                ):
                    return redirect(to=form_path)
