import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Content
from .forms import UploadForm, EditForm
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
            context = form.save(commit=False)
            context.created_by = now_user
            context.updated_by = now_user
            context.created_at = now_time
            context.updated_at = now_time
            context.save()
            return redirect(to='otherdocs:index')
    params = {
        'form': form
    }
    return render(request, 'otherdocs/upload.html', params)

@login_required()
def EditIndexView(request):
    now_user = request.user
    if not OtherDocsPermission(now_user):
        return redirect(to='otherdocs:index')
    contents = Content.objects.all().order_by(
        'index', 'updated_at'
    ).reverse()
    params = {
        'contents': contents,
    }
    return render(request, 'otherdocs/edit_index.html', params)

@login_required()
def EditView(request, pk):
    now_user = request.user
    if not OtherDocsPermission(now_user):
        return redirect(to='otherdocs:index')
    content = get_object_or_404(Content, pk=pk)
    form = EditForm(request.POST or None, request.FILES or None, instance=content)
    if (request.method == 'POST'):
        if form.is_valid():
            if form.cleaned_data['delete']:
                content.delete()
                messages.success(request, content.title + 'を削除しました')
                return redirect(to='otherdocs:edit_index')
            now_time = datetime.datetime.now()
            context = form.save(commit=False)
            context.updated_by = now_user
            context.updated_at = now_time
            context.save()
            messages.success(request, content.title + 'を更新しました')
            return redirect(to='otherdocs:edit_index')
    params = {
        'form': form
    }
    return render(request, 'otherdocs/edit.html', params)
