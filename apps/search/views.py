from django.shortcuts import render

# Create your views here.
from movie.models import MovieInfo
from elasticsearch import Elasticsearch
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def movie_search(request):
    query = request.POST.get('q', '')
    movie_name, movie_id = fulltextsearch(query)
    print('full text search num: {}'.format(len(movie_id)))

    movie_list = []
    for movieid in movie_id:
        movie = MovieInfo.objects.get(id=int(movieid))
        movie_list.append(movie)
        #此部分功能建议上线后再调试
    paginator = Paginator(movie_list, 8)
    page = request.GET.get('page')
    search_movie = paginator.get_page(page)
    return render(request, 'es.html', {
        "search_movie": search_movie
    })


def fulltextsearch(request):
    es = Elasticsearch({"39.98.134.232:9200"})
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
