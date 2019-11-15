
import datetime
import happybase

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from user.models import UserProfile
# 电影的存储未考虑切分演员，导演等等
# # 电影类型表，貌似没用
# class MovieCategory(models.Model):
#     category = models.CharField(max_length=100, default='', verbose_name='电影类型')
#     movienum = models.IntegerField(default=0, verbose_name='对应电影数量')
#
#     def __str__(self):
#         return self.category
#
#     class Meta:
#         verbose_name = '电影类型'
#         verbose_name_plural = verbose_name

# 电影详情表
class MovieInfo(models.Model):

    # 是否要豆瓣id设置为主键？

    RATING_RANGE = (
        MaxValueValidator(5),
        MinValueValidator(0)
    )
    moviename = models.CharField(max_length=1000, default='', verbose_name='片名')
    directors = models.CharField(max_length=1000, default='', verbose_name='导演', null=True, blank=True)
    editors = models.CharField(max_length=255, default='', verbose_name='编剧', null=True, blank=True)
    leadactors = models.CharField(max_length=1000, default='', verbose_name='主演', null=True, blank=True)
    nation = models.CharField(max_length=255, default='', verbose_name='国家', null=True, blank=True)
    language = models.CharField(max_length=255, default='', verbose_name='语言', null=True, blank=True)
    releasedate = models.DateField(default=datetime.datetime.now, verbose_name='上映年份', null=True, blank=True)
    othername = models.CharField(max_length=1000, default='', verbose_name='又名', null=True, blank=True)
    description = models.TextField(default='', verbose_name='简介', null=True, blank=True)
    durations = models.CharField(max_length=255, default='', verbose_name='片长', null=True, blank=True)
    # 未得到
    numrating = models.IntegerField(default=0, verbose_name='评分人数', null=True, blank=True)
    typelist = models.CharField(max_length=255,default='', verbose_name='类型',null=True,blank = True)
    averating = models.FloatField(default=0, validators=RATING_RANGE, verbose_name='评分(0-5)', null=True, blank=True)
    # #     /*proccess*/ 貌似也没用
    # if averating > models.FloatField(0) and averating < models.FloatField(1):
    #     rating = "rating05"
    # elif averating > models.FloatField(1) and averating < models.FloatField(2):
    #     rating = "rating15"
    # elif averating > models.FloatField(2) and averating < models.FloatField(3):
    #     rating = "rating25"
    # elif averating > models.FloatField(3) and averating < models.FloatField(4):
    #     rating = "rating35"
    # elif averating > models.FloatField(4) and averating < models.FloatField(5):
    #     rating = "rating45"
    # else:
    #     rating = "rating" + str(averating) + str(0)

    # 和刘德xin对接一下，picture部分要用什么Field
    picture = models.CharField(max_length=1000, verbose_name='缩略图', null=True, blank=True,
                               default='/static/img/m16.jpg')
    backpost = models.CharField(max_length=3000, verbose_name='详情页海报', null=True, blank=True,
                                default='/static/img/m16.jpg')

    def __str__(self):
        return '%s - %s - %s - %s - %lf - %s' % (
        self.directors, self.moviename, self.nation, self.releasedate, self.averating, self.picture)

    class Meta:
        verbose_name = '电影信息'
        verbose_name_plural = verbose_name

# 电影相似度表
class MovieSimilar(models.Model):
    item1 = models.IntegerField(default=0, verbose_name='电影id')
    item2 = models.IntegerField(default=0, verbose_name='电影id')

    similar = models.FloatField(default=0, verbose_name='相似度')

    def __str__(self):
        return '%d - %d - %lf' % (self.item1, self.item2, self.similar)

    class Meta:
        verbose_name = '电影相似度信息'
        verbose_name_plural = verbose_name

# 用户评论以及电影评分表
# 一条评论是属于一个用户对一个电影的，所以user和movie都是多对一，使用ForeignKey
class Review(models.Model):
    def __init__(self):
        connection = happybase.Connection(host='39.100.88.119', port=9090)
        connection.open()


    # STAR_RANGE = [
    #     MaxValueValidator(5),
    #     MinValueValidator(0)
    # ]
    # # int
    # user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    # # int
    # movie = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    # # str
    # content = models.TextField(max_length=255, default='', verbose_name='评论', null=True, blank=True)
    # # float
    # star = models.FloatField(default=0, validators=STAR_RANGE, verbose_name='星级')
    # # datetime.datetime
    # reviewtime = models.DateTimeField(default=datetime.datetime.now, verbose_name='提交时间')

    # connection = happybase.Connection(host='39.100.88.119', port=9090)
    # connection.open()
    # # tableList = connection.tables()
    # # comment_table = happybase.Table('comment', connection)
    # # row = comment_table.row('10344754_https://www.douban.com/people/119429128/')
    # # region = comment_table.regions()
    # query_str = "RowFilter (=, 'regexstring:26752088*')"
    # query = comment_table.scan(filter=query_str, limit=1000)
    # result = list(query)
    # connection.close()

    def getComments(movie_id):
        comment_table = happybase.Table('comment', self.connection)
        query_str = "RowFilter (=, 'substring:_" + movie_id + "')"
        query = comment_table.scan(filter=query_str, limit=1000)
        result = list(query)
        print(result)


    def hasUserComment(movie_id, user_id):
        comment_table = happybase.Table('comment_local', self.connection)
        query_str = "RowFilter (=, 'binary:" + user_id + "_" + movie_id + "')"
        query = comment_table.scan(filter=query_str, limit=1000)
        result = list(query)
        if len(result) == 0:
            return False
        else:
            return True


    def addComment(movie_id, user_id, content, star):
        comment_table = happybase.Table('comment_local', self.connection)
        if hasUserComment(movie_id, user_id):
            return False
        comment_table.put(user_id + "_" + movie_id, {"region:content": content, "region:star": star})


    def deleteComment(movie_id, user_id):
        comment_table = happybase.Table('comment_local', self.connection)
        comment_table.delete(user_id + "_" + movie_id)


    def free():
        self.connection.close()


    # def __str__(self):
    #     return '%s - %s - %lf' % (self.user.username, self.movie.moviename, self.star)

    # class Meta:
    #     verbose_name = '用户打分及评论'
    #     verbose_name_plural = verbose_name


