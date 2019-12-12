import os
from io import BytesIO
from django.http import HttpResponse
import urllib.parse


def download(filepath, filename, mimetype):
    file = open(filepath, 'rb')
    response = HttpResponse(
        file,
        status=200, 
        content_type=mimetype
        )
    response['Content-Disposition'] = 'attachment; filename="{fn}"'.format(fn=urllib.parse.quote(filename))
    return response

