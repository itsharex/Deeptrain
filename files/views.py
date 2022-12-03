from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, FileResponse, JsonResponse, Http404
from django.shortcuts import render
from django.core.paginator import Paginator
from views import login_required, ajax_required
from .forms import FileForm
from .models import *


@login_required
def index(request: WSGIRequest, _) -> HttpResponse:
    return render(request, "files/index.html")


@login_required
def upload(request: WSGIRequest, user) -> HttpResponse:
    if request.POST or request.is_ajax():
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
        file = UserFile.objects.get(user_bind=uid, uuid_name=ufile).real_name
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
        objs = UserFile.objects.filter(real_name__icontains=name).order_by("id") if name \
            else UserFile.objects.order_by("id")
        page_query = int(request.GET.get("page", 0))
        page = Paginator(objs, 10)
        resp = page.get_page(page_query)

        return JsonResponse({
            "data": [obj.to_jsonable for obj in resp],
            "total": page.num_pages,
        })
    except ValueError as err:
        raise Http404("Value Error") from err
