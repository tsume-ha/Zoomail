import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .models import Content
from .forms import UploadForm
from utils.commom import download
from config.permissions import OtherDocsPermission

@login_required()
def index(request):
    contents = Content.objects.all().order_by(
        'index', 'updated_at'
    ).reverse()
    params = {
        'contents': contents,
        'can_edit': OtherDocsPermission(request.user)
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
    now_user = request.user
    if not OtherDocsPermission(now_user):
        return redirect(to='otherdocs:index')
    form = UploadForm(request.POST or None, request.FILES or None)
    if (request.method == 'POST'):
        if form.is_valid():
            now_time = datetime.datetime.now()
            content = form.save(commit=False)
            content.created_by = now_user
            content.updated_by = now_user
            content.created_at = now_time
            content.updated_at = now_time
            content.save()
            return redirect(to='otherdocs:index')
    params = {
        'form': form
    }
    return render(request, 'otherdocs/upload.html', params)
