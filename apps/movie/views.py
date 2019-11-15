from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# from operation.views import recommendForUser
from .models import MovieInfo, MovieSimilar, Review

# Create your views here.
from django.views import View
from django.http import HttpResponse
import json
# 设调取豆瓣评论的API为 douban()

class ContentView(View):

    def get(self, request, movie_id):
        movieinfo = MovieInfo.objects.get(id=movie_id)

        # 对用户进行的个性化推荐，user_recommend_movies显示在电影详情页右侧

        # 判断用户是否已经给电影打分了。如果已打分则返回打分分数
        all_comments = None
        rating_star = 0
        try:
            movie = Review.objects.get(movie_id=movie_id, user_id=request.user.id)
            rating_star = movie.star
        except:
            pass

        # douban_review = douban(movie_id)


        all_comments = Review.objects.filter(movie_id=movie_id)

        # 相似电影
        similar_movies_ids = MovieSimilar.objects.filter(item1=movie_id).order_by('-similar')
        similar_movies = list(map(lambda x: MovieInfo.objects.get(id=x.item2), similar_movies_ids))



        return render(request, 'movie_detail.html', {"movie": movieinfo,
                                                "recommend_list": similar_movies[0: 8],
                                                     # 这里用recommend_list 代替了similar
                                                "review_list": all_comments,
                                                # "douban_review" :douban_review
                                                "form": Review()
                                                })


class AddReview(View):
    # 用户添加用户评论，未考虑多次评论和打分
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail",",msg":"用户未登陆"}', content_type='application/json')


        user = request.user
        movie_id = request.POST.get("movie_id", '0')
        comments = request.POST.get("comments", "")
        star = request.POST.get("star", '1')

        # comment = Review.objects.hasUserComment(movie_id=movie_id, user_id=user)
        # if comment:
        #     return render(request, 'review_fail.html', {'msg':json.dumps({"msg": ("您已经评论过，不能再评论")})})

        if int(movie_id) > int(0) and comments:
            movie_comments = Review()
            comment = movie_comments.hasUserComment(movie_id=movie_id, user_id=user)
            if comment:
                return render(request, 'review_fail.html', {'msg':json.dumps({"msg": ("您已经评论过，不能再评论")})})
            movie_comments.addComment(movie_id=movie_id, user_id=user, content=comments, star=float(star))
            movie_comments.free()
            # movie = MovieInfo.objects.get(id=movie_id)
            # movie_comments.movie = movie
            # movie_comments.content = comments
            # movie_comments.user = request.user
            # movie_comments.star = float(star)
            # # movie_comments.user_id = 1
            # # movie_comments.movie_id = 2
            # # movie_comments.content = 'hello'
            # # movie_comments.star = 3.0
            # movie_comments.save()
            #需要修改
            return render(request, 'review_ok.html',{'msg':json.dumps({"msg": ("评论成功")})})
        else:
            return render(request, 'review_fail.html',{'msg':json.dumps({"msg": ("评论失败，请重新尝试")})})


class DeleteReview(View):
    def post(self,request):
        user = request.user
        movie_id = request.POST.get("movie_id", '0')
        movie_comments = Review()
        comment = movie_comments.hasUserComment(movie_id=movie_id, user_id=user)
        if not comment:
            return render(request, 'review_fail.html', {'msg':json.dumps({"msg": ("您还未进行评论")})})
        movie_comments.deleteComment(movie_id=movie_id, user_id=user)
        movie_comments.free()
        # Review.objects.filter(user_id=user,movie_id=movie_id).delete()
        return render(request, 'review_ok.html', {'msg':json.dumps({"msg": ("删除评论成功")})})
