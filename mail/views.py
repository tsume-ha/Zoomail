from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from .models import MailLog
from django.conf import settings

MAIL_STATUS_API_KEY = settings.MAIL_STATUS_API_KEY


class MailStatusView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        # confirm x-auth header
        auth_header = request.META.get("HTTP_X_AUTHORIZATION")
        if auth_header != MAIL_STATUS_API_KEY:
            return HttpResponseForbidden()

        message_id = request.GET.get("message_id")
        if not message_id:
            return HttpResponseBadRequest()

        try:
            log = MailLog.objects.get(mail_id=message_id)
        except MailLog.DoesNotExist:
            return HttpResponseBadRequest()

        return JsonResponse(
            {
                "message_id": log.mail_id,
                "status": log.status,
            }
        )

    @csrf_exempt
    def post(self, request):
        auth_header = request.META.get("HTTP_X_AUTHORIZATION")
        if auth_header != MAIL_STATUS_API_KEY:
            return HttpResponseForbidden()

        try:
            message_id = request.POST.get("message_id")
            status = request.POST.get("status")
            error_message = request.POST.get("error_message")

        except KeyError:
            return HttpResponseBadRequest()
        if not message_id or not status:
            return HttpResponseBadRequest()

        try:
            log = MailLog.objects.get(mail_id=message_id)
        except MailLog.DoesNotExist:
            return HttpResponseBadRequest()

        log.status = status
        log.error = error_message
        log.save()

        return JsonResponse(
            {
                "message_id": log.mail_id,
                "status": log.status,
            }
        )
