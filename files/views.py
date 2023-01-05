from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, FileResponse, JsonResponse, Http404
from django.shortcuts import render
import files.models
from DjangoWebsite.settings import FILE_PERMISSION_LEVEL
from utils.wraps import login_required, identity_required, ajax_required
from .forms import FileForm
from .models import *
from .cache import fileCache


@login_required
def index(request: WSGIRequest, _) -> HttpResponse:
    return render(request, "files/index.html")


@identity_required(FILE_PERMISSION_LEVEL)
def upload(request: WSGIRequest, user) -> HttpResponse:
    if request.POST:
        form = FileForm(user, request.POST, request.FILES)
        if form.is_valid():
            return JsonResponse({
                "success": True,
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
        try:
            file = UserFile.objects.get(user=uid, uuid_name=ufile).real_name
        except files.models.UserFile.MultipleObjectsReturned:  # get() returned more than one UserFile -- it returned 2!
            file = UserFile.objects.filter(user=uid, uuid_name=ufile).first().real_name
        return FileResponse(
            open(directory, "rb"),
            as_attachment=True,
            filename=file,
        )
    else:
        raise Http404("File does not exists.")


@ajax_required
@login_required
def search(request: WSGIRequest, _):
    try:
        name = str(request.GET.get("name", "")).strip()
        page_query = int(request.GET.get("page", 0))
        num_pages, page = fileCache(name, page_query, (),)

        return JsonResponse({
            "data": [obj.json for obj in page],
            "total": num_pages,
        })
    except ValueError as err:
        raise Http404("Value Error") from err
