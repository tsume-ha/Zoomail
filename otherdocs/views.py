from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Content
from .forms import UploadForm
from utils.commom import download

@login_required()
def index(request):
    contents = Content.objects.all().order_by(
        'index', 'updated_at'
    ).reverse()
    params = {
        'contents': contents
    }
    return render(request, 'otherdocs/index.html', params)

@login_required()
def FileDownloadView(request, pk):
    content = get_object_or_404(Content, pk=pk)
    filename = content.title + content.extension()
    response = download(
        filepath=content.file.path,
        filename=filename,
        mimetype='application/octet-stream'
    )
    return response


@login_required()
def UploadView(request):
    form = UploadForm(request.POST or None, request.FILES or None)

    params = {
        'form': form
    }
    return render(request, 'otherdocs/upload.html', params)
