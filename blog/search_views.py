from django.http import JsonResponse
from haystack.views import SearchView


class BlogSearchView(SearchView):
    template = "blog/search.html"

    @property
    def drf_context(self):
        return JsonResponse(super().get_context(), safe=True)
