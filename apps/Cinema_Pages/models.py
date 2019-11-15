import time
import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from movie.models import MovieInfo
from user.models import UserProfile

class DefaultRecom(models.Model):
    movie = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    # movie = models.IntegerField(default=0, verbose_name='电影id')
    redate = models.DateField(default=datetime.datetime.now, verbose_name='推荐时间')

    def __str__(self):
        return str(self.movie_id)

    class Meta:
        verbose_name = '默认电影推荐'
        verbose_name_plural = verbose_name


#
# class StaRecom(models.Model):
#
#     movie = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
#     user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
#     rating = models.FloatField(default=0, verbose_name='评分')
#
#     def __str__(self):
#         return '%s - %s -%lf' % (self.user, self.movie, self.rating)
#         # return '%s - %s -%lf' % (self.userid, self.movieid, self.rating)
#
#     class Meta:
#         verbose_name = '用户推荐信息'
#         verbose_name_plural = verbose_name
#
#


