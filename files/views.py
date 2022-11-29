from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, FileResponse, JsonResponse, Http404
from django.shortcuts import render
from views import login_required
from .forms import FileForm
from .models import *


@login_required
def upload(request: WSGIRequest, user) -> HttpResponse:
    if request.POST or request.is_ajax():
        form = FileForm(user, request.POST, request.FILES)
        if form.is_valid():
            return JsonResponse({
                "success": True,
                "name": str(form.get_file()),  # throw Object of type InMemoryUploadedFile is not JSON serializable
                "link": form.get_link(),
            })

        else:
            return JsonResponse({
                "success": False,
                "error": form.get_error(),
            })
    else:
        return render(request, "files/upload.html", {
            "form": FileForm(user),
            "max_size": MAX_FILE_SIZE,
            "max_name": MAX_FILE_NAME_LENGTH,
        })


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
