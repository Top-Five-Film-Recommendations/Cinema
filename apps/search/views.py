from django.shortcuts import render

# Create your views here.
from movie.models import MovieInfo
from elasticsearch import Elasticsearch
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

es_addr = "39.98.134.232:9200"

class MovieSearch(View):


    def get(self,request):
        page = request.GET.get('page')
        search_movie = (pagi).get_page(page)
        return render(request, 'movie_display.html', {
            "commend_movie": search_movie
        })

    def post(self,request):
        query = request.POST.get('q', '')
        movie_name, movie_id = fulltextsearch(query)
        print('full text search num: {}'.format(len(movie_id)))
        for i in range(0, len(movie_id)):
            movie_id[i] = int(movie_id[i])
        # movie_list = MovieInfo.objects.filter(id__in=movie_id)
        movie_list = []
        for movieid in movie_id:
            movie = MovieInfo.objects.get(id=int(movieid))
            movie_list.append(movie)
        paginator = Paginator(movie_list, 8)
        page = request.GET.get('page')
        search_movie = paginator.get_page(page)
        global pagi
        pagi = paginator
        return render(request, 'movie_display.html', {
            "commend_movie": search_movie
        })


def movie_search(request):
    query = request.GET.get('q', '')
    movie_name, movie_id = fulltextsearch(query)
    print('full text search num: {}'.format(len(movie_id)))
    for i in range(0,len(movie_id)):
        movie_id[i] = int(movie_id[i])
    # movie_list = MovieInfo.objects.filter(id__in=movie_id)
    movie_list = []
    for movieid in movie_id:
        movie = MovieInfo.objects.get(id=int(movieid))
        movie_list.append(movie)
    #     #此部分功能建议上线后再调试
    paginator = Paginator(movie_list, 8)
    page = request.GET.get('page',default='1')
    # search_movie = paginator.page(page)
    # 根据页码从分页器中取出对应页的数据
    try:
        search_movie = paginator.page(page)
    except PageNotAnInteger as e:
        # 不是整数返回第一页数据
        search_movie = paginator.page('1')
        page = 1
    return render(request, 'movie_display.html', {
        "commend_movie": search_movie
    })


def fulltextsearch(request):
    es = Elasticsearch({es_addr})
    ret = es.search(index="movieinfo"
                    ,body= {
            "_source": ["name"],
            "query": {
                "bool": {
                    "should": [
                        {
                            "function_score": {
                                "query": {
                                    "bool": {
                                        "should": [
                                            {
                                                "term": {
                                                    "actor": request
                                                }
                                            },
                                            {
                                                "term": {
                                                    "writer": request
                                                }
                                            },
                                            {
                                                "term": {
                                                    "director": request
                                                }
                                            }
                                        ],
                                        "minimum_should_match": 1,
                                        "boost": 1
                                    }
                                },
                                "boost": 0.8
                            }
                        },
                        {
                            "function_score": {
                                "query": {
                                    "multi_match": {
                                        "query": request,
                                        "type": "best_fields",
                                        "fields": [
                                            "name^8",
                                            "brief",
                                            "alias^2"
                                        ],
                                        "tie_breaker": 0.3,
                                        "minimum_should_match": "30%"
                                    }
                                },
                                "boost": 0.2
                            }
                        }
                    ]
                }
            },"size":1000
        }
                    )
    resultback = ret["hits"]["hits"]
    names = []
    ids = []
    for hit in resultback:
        names.append(hit['_source']['name'])
        ids.append(hit["_id"])
    # print(names)
    # print(ids)
    print('search result num: {}'.format({len(names)}))
    return names,ids
