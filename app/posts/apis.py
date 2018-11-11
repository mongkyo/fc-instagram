import json

from django.http import HttpResponse

from .models import HashTag


def tag_search(request):
    # URL: '/posts/api/tag-search/'
    # request.GET으로 전달된
    #  search_keyword값을 가지는(contains)
    #  HashTag목록을
    #  dict요소의 list로 만들어 HttpResponse에 리턴
    #  ex) [{}, {}, {}]
    keyword = request.GET.get('keyword', '')
    tags = []
    if keyword:
        tags = list(HashTag.objects.filter(name__istartswith=keyword).values())
    result = json.dumps(tags)
    return HttpResponse(result, content_type='application/json')
