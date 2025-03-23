import os
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import File
from .forms import FileUploadForm


@login_required
def file_list(request):
    files = File.objects.all()
    view_mode = request.GET.get("view", "list")
    print(files)
    return render(
        request, "others/file_list.html", {"files": files, "view_mode": view_mode}
    )


@login_required
def file_detail(request, pk):
    file = get_object_or_404(File, pk=pk)
    return render(request, "others/file_detail.html", {"file": file})


@login_required
def file_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.upload_user = request.user
            file_instance.original_name = request.FILES["file"].name
            file_instance.save()
            return redirect("others:file_list")
    else:
        form = FileUploadForm()
    return render(request, "others/file_upload.html", {"form": form})


@login_required()
def file_download(request, content_id):
    content = get_object_or_404(File, id=content_id)
    filename = content.filename + os.path.splitext(content.file.name)[1]
    return FileResponse(
        open(content.file.path, "rb"), as_attachment=False, filename=filename
    )
