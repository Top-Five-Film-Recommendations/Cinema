# -*- coding: UTF-8 -*-

from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views import View
import random
# new
from movie.models import Review, MovieInfo,MovieSimilar
from Cinema_Pages.models import DefaultRecom
from user.models import UserProfile
from django.db.models import Q
from elasticsearch import Elasticsearch
import happybase

# old
# from .func import fuzzy_finder
# from .func import GetOtherInfo
# from .forms import ReviewForm
import MySQLdb

elasticsearch_IP_PORT = "39.98.134.232:9200"
HBASE_IP = '39.100.88.119'
# 首页
def index(request):
    return render(request, 'index.html')

# 推荐函数，包括默认推荐和用户推荐
# 未做：协同过滤和用户登录后的推荐


def sortAverating(val):
    return val[1]

def calDefaultRecom(request):
    # 24部评分最高，24部最新
    # 这里或许应该在设立一个id功能来
    # 每一个example对应的导演、主演只有一个
    tmp_title_list = []
    title_list = []

    recom_tuple = []
    lim_len_rate = 48
    len_index_rate = 0
    lim_len_date = 24
    len_index_date = 0


    all_movieinfo_rate = MovieInfo.objects.all().order_by('-numrating')
    for movie in all_movieinfo_rate:
        if (lim_len_rate > len_index_rate):
            if (movie.id not in tmp_title_list):
                tmp_title_list.append(movie.id)
                recom_tuple.append((movie.id, movie.averating))
                len_index_rate += 1
            else:
                continue
        else:
            break

    recom_tuple.sort(key = sortAverating, reverse = True)
    for i in range(0,int(min(len(recom_tuple), lim_len_date))):
        title_list.append(recom_tuple[i][0])


    all_movieinfo = MovieInfo.objects.all().order_by('-releasedate')

    for movie in all_movieinfo:
        if (lim_len_date > len_index_date):
            if movie.id not in title_list:
                title_list.append(movie.id)
                len_index_date += 1
            else:
                continue
        else:
            break

    #将当前默认推荐删除
    DefaultRecom.objects.filter().delete()

    for mvid in title_list:
        defaultrecom = DefaultRecom()
        defaultrecom.movie = MovieInfo.objects.get(id = mvid)
        defaultrecom.save()

    default_recommend_movies = DefaultRecom.objects.all()
    user_recommend_movies = default_recommend_movies
    movie_list = []
    for mv in user_recommend_movies:
        movie_list.append(mv.movie)
    paginator = Paginator(movie_list, 8)
    page = request.GET.get('page')
    movies = paginator.get_page(page)


    return render(request, 'movie_display.html', {
        "commend_movie": movies
    })


# def sortThird(val):
#     return val[2]

'''
#  基于统计的对用户的推荐
# def calStaRecom(current_user_id):
#     # 遍历review表，提取current user的前8个最近评价的电影。
#     movie_comments = Review()
#     reviews_descend = Review.objects.all().filter(user_id=current_user_id).order_by('-reviewtime')
# 
#     # 取前8个最近的评价
#     if len(reviews_descend) > 50:
#         # top_list.append(reviews_descend[i].movie_id)
#         reviews_descend = reviews_descend[0: 25]
# 
#     # 对前8个最近的评价按star排序
# 
#     # convert query to list
#     tuple_list = []
#     for review in reviews_descend:
#         tuple_ = (review.user_id, review.movie_id, review.star)
#         tuple_list.append(tuple_)
# 
#     tuple_list.sort(key=sortThird, reverse=True)
# 
#     if len(tuple_list) > 8:
#         tuple_list = tuple_list[0: 8]
# 
#     # 取Movie_id
#     top_list = []
#     for review in tuple_list:
#         top_list.append(review[1])
# 
#     # 每个movie_id对应取得similar movie 的个数
#     num_every_top = 2
#     # 对多个高分评价电影，遍历similarity表，匹配最相似的电影，存储进Top8Recommend表。
# 
#     # 8个相似推荐
#     recommend_list = []
#     for i in range(len(top_list)):
#         recommend_queryset = MovieSimilar.objects.filter(
#             Q(item1__in=[top_list[i]]) | Q(item2__in=[top_list[i]])).order_by('-similar')[: num_every_top]
#         for item in recommend_queryset:
# 
#             # 只推荐16个
#             if len(recommend_list) == 16:
#                 break
# 
#             if (item.item1 == top_list[i]) and (item.item2 not in recommend_list):
#                 recommend_list.append(item.item2)
#             if (item.item2 == top_list[i]) and (item.item1 not in recommend_list):
#                 recommend_list.append(item.item1)
#         # 只推荐8个
#         if len(recommend_list) == 16:
#             break
# 
#     '''
#     # 新用户，个性推荐不足8个
#     if len(recommend_list) < 8:
#         queryset = Default5Recommend.objects.all()
#         for movie in queryset:
#             if len(recommend_list) < 8 and movie.movie_id not in recommend_list:
#                 recommend_list.append(movie.movie_id)
#    '''
#
#     # 将当前用户的往期相似推荐删除
#     StaRecom.objects.filter(user_id=current_user_id).delete()
#
#     # 将recommend_list 存进 Top8Recommend
#     # print ('****------*******\n recommend_list : ',recommend_list)
#     for movie_id in recommend_list:
#         starecom = StaRecom()
#         movie = MovieInfo.objects.get(id=movie_id)
#         user = UserProfile.objects.get(id=current_user_id)
#         starecom.movie = movie
#         starecom.user = user
#         starecom.save()
#
#     movie_comments.free()



class Cinema_Pages_view(View):
    def get(self, request):
        user_recommend_movie = DefaultRecom.objects.all()
        movie_list = []
        for movie in user_recommend_movie:
            movie_list.append(movie.movie)
        paginator = Paginator(movie_list, 8)
        page = request.GET.get('page')
        movies = paginator.get_page(page)

        return render(request, 'movie_display.html', {
            "commend_movie": movies
        })


def reCal_spark(request):
    pass



def movie_type(request, type):
    movie_name, movie_id = searchByType(type)
    for i in range(0,len(movie_id)):
        movie_id[i] = int(movie_id[i])
    # print('full text search num: {}'.format(len(movie_id)))
    movie_list = MovieInfo.objects.filter(id__in=movie_id)
    # movie_list = []
    # for movieid in movie_id:
    #     movie = MovieInfo.objects.get(id=int(movieid))
    #     movie_list.append(movie)
        # 此部分功能建议上线后再调试，因为主键不能修改
    paginator = Paginator(movie_list, 8)
    page = request.GET.get('page')
    commend_movie = paginator.get_page(page)

    return render(request, 'movie_display.html', {
        "commend_movie": commend_movie
    })



def searchByType(request):
    es = Elasticsearch({HBASE_IP})
    ret = es.search(index="movieinfo"
                    , body={
            "_source": ["name"],
            "query": {
                "term": {
                    "type": request
                }
            },
            "sort": [
                {
                    "score": {
                        "order": "desc"
                    }
                }
            ],
            "size": 1000
        })
    resultback = ret["hits"]["hits"]
    names = []
    ids = []
    # print(len(resultback))
    for hit in resultback:
        names.append(hit['_source']['name'])
        ids.append(hit["_id"])
    # print(names)
    # print(ids)
    print('search result num: {}'.format(len(names)))
    return names, ids

def ucf_recom(request):
    user_id = request.user.id
    movie_id_str = ucf(user_id)
    movie_list = []
    if len(movie_id_str)>0:
        movie_id_list = movie_id_str.split(',')
        for movie_id in movie_id_list:
            tmp = MovieInfo.objects.get(id=int(movie_id))
            movie_list.append(tmp)
    paginator = Paginator(movie_list, 8)
    page = request.GET.get('page')
    commend_movie = paginator.get_page(page)
    return render(request, 'movie_display.html', {
        "commend_movie": commend_movie
    })

# 这是ucf 即接口函数
def ucf(user_id):
    connection = happybase.Connection(host=HBASE_IP, port=9090)
    connection.open()
    recommend_table = happybase.Table('recommend', connection)
    tmp = recommend_table.row(str(user_id))
    movie_id = ''
    for key, value in tmp.items():
        movie_id = value.decode('utf-8')
    connection.close()
    return movie_id
