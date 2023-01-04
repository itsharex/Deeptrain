from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from haystack.views import SearchView
from .models import Article, Comment
from DjangoWebsite.settings import BLOG_PAGINATION
from views import throw_bad_request


def boolean_to_javascript(val):
    return "true" if val else "false"


class BlogSearchView(SearchView):
    template = "blog/index.html"

    @property
    def drf_context(self):
        return JsonResponse(super().get_context(), safe=True)

    def __call__(self, request: WSGIRequest):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """

        query = request.GET.get("q")
        if not query:
            pagination = Paginator(Article.objects.order_by("id"), BLOG_PAGINATION)
            page = pagination.page(request.GET.get("page", 1))
            return render(request, self.template, {"page": page, "query": ""})
        else:
            return super().__call__(request)


def article(request: WSGIRequest, idx):
    if idx >= 0:
        query = Article.objects.filter(id=idx)
        if query.exists():
            article_instance = query.first()
            state = request.user.is_authenticated and request.user in article_instance.likes.all()
            return render(request, "blog/article.html", {
                "article": article_instance,
                "state": boolean_to_javascript(state),
                "comments": Comment.objects.filter(article=article_instance),
            })
    return throw_bad_request(request, "请求的博客不存在")


def like(request: WSGIRequest, idx: int):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(
            {"success": False, "reason": "您还未登录, 请先 <a href='/login/' class='layui-font-blue'>登录</a>"})

    query = Article.objects.filter(id=idx)
    if not query.exists():
        return JsonResponse({"success": False, "reason": "请求的博客不存在"})
    article_instance = query.first()
    state = request.user in article_instance.likes.all()
    if state:
        article_instance.likes.remove(user)
    else:
        article_instance.likes.add(user)
    return JsonResponse({"success": True, "state": not state, "number": article_instance.likes_number})


def comment(request: WSGIRequest, idx: int):
    """

    :param request: WSGIRequest
    :param idx: article id [int]
    :method POST
        - `content`: comment content [str]
        - `parent` (Optional): parent comment id [int]

    :return: JsonResponse
    """
    content = request.POST.get("content", "").strip()[:300]
    if not content:
        return JsonResponse({"success": False, "reason": "评论内容为空"})

    user = request.user
    if not user.is_authenticated:
        return JsonResponse(
            {"success": False, "reason": "您还未登录, 请先 <a href='/login/' class='layui-font-blue'>登录</a>"})

    query = Article.objects.filter(id=idx)
    if not query.exists():
        return JsonResponse({"success": False, "reason": "请求的博客不存在"})
    article_instance = query.first()

    parent_id: str = request.POST.get("parent", None)
    if parent_id and parent_id.isdigit():
        parent_query = Comment.objects.filter(id=int(parent_id))
        if not parent_query.exists():
            return JsonResponse({"success": False, "reason": "回复的评论不存在"})
        parent_comment = parent_query.first()
        root = parent_comment.get_root()  # 将回复的二级评论转为此评论的根评论实例, 即最大支持二级目录
        comment_id = Comment.objects.create(content=content, article=article_instance, user=user, parent=root,
                                            reply_to=parent_comment.user if parent_comment != root else None).id
        return JsonResponse({"success": True, "id": comment_id})

    comment_id = Comment.objects.create(content=content, article=article_instance, user=user).id
    return JsonResponse({"success": True, "id": comment_id})
