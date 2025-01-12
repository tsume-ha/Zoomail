import urllib.parse
from django.http import FileResponse, HttpResponseNotFound


def file_response_or_404(filepath, filename, mimetype):
    try:
        response = FileResponse(
            open(filepath, "rb"),
            as_attachment=True,
            filename=urllib.parse.quote(filename),
        )
        response["Content-Type"] = mimetype  # 必要な場合、明示的に設定
        return response
    except FileNotFoundError:
        return HttpResponseNotFound("File not found")
