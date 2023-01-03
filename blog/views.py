from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render
from .models import Article
from DjangoWebsite.settings import BLOG_PAGINATION
from django.core.paginator import Paginator
from views import throw_bad_request


def boolean_to_javascript(val):
    return "true" if val else "false"


def index(request: WSGIRequest):
    pagination = Paginator(Article.objects.all(), BLOG_PAGINATION)
    page = pagination.page(request.GET.get("page", 1))
    return render(request, "blog/index.html", {"paginator": page, "total": pagination.num_pages})


def article(request: WSGIRequest, idx):
    if idx >= 0:
        query = Article.objects.filter(id=idx)
        if query.exists():
            article_instance = query.first()
            state = request.user.is_authenticated and request.user in article_instance.likes.all()
            return render(request, "blog/article.html", {
                "article": article_instance,
                "state": boolean_to_javascript(state)
            })
    return throw_bad_request(request, "请求的博客不存在")


def like(request: WSGIRequest, idx):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"success": False, "reason": "您还未登录, 请先 <a href='/login/' class='layui-font-blue'>登录</a>"})
    query = Article.objects.filter(id=idx)
    if query.exists():
        article_instance = query.first()
        state = request.user in article_instance.likes.all()
        if state:
            article_instance.likes.remove(user)
        else:
            article_instance.likes.add(user)
        return JsonResponse({"success": True, "state": not state, "number": article_instance.likes_number,
                             "reason": "操作成功"})
    return JsonResponse({"success": False, "reason": "请求的博客不存在"})
