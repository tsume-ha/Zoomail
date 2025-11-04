from utils.file_response import file_response_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

from mail.models import Message, Attachment
from mail.utils import can_read_message


@require_http_methods(["GET"])
@login_required
def download(request, message_id, attachment_id):
    try:
        message = Message.objects.get(pk=message_id)
        file = Attachment.objects.get(pk=attachment_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("File not found")

    if not can_read_message(message, request.user):
        return HttpResponseNotFound("File not found")

    response = file_response_or_404(
        filepath=file.file.path,
        filename=file.org_filename,
        mimetype="application/octet-stream",
    )
    return response
