from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render
from views import login_required
from .forms import FileForm
from .models import *


@login_required
def upload(request: WSGIRequest, user) -> HttpResponse:
    if request.POST:
        form = FileForm(user, request.POST, request.FILES)
        if form.is_valid():
            return render(request, "files/upload.html", {
                "form": form,
                "name": form.get_file(),
                "link": form.get_link(),
            })
        else:
            return render(request, "files/upload.html", {"form": FileForm(user), "error_code": form.get_error()})
    else:
        return render(request, "files/upload.html", {"form": FileForm(user)})


@login_required
def download(request: WSGIRequest, _, uid: int, ufile: str) -> FileResponse:
    directory = get_directory(uid, ufile)
    if os.path.exists(directory):
        file = UserFile.objects.get(user_bind=uid, uuid_name=ufile).real_name
        return FileResponse(
            open(directory, "rb"),
            as_attachment=True,
            filename=file,
        )
    else:
        raise Http404("File does not exists.")
