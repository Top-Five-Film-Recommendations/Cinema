from django.shortcuts import render

# Create your views here.
from movie.models import MovieInfo
from elasticsearch import Elasticsearch

def get_search_dict(request):
    search_dic = {}
    return search_dic
def movie_search(request):
    search_dic = get_search_dict(request)
    movie = MovieInfo.objects


