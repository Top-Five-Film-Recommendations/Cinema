
import datetime
import happybase

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from user.models import UserProfile

es_ip_port = 
hbase_ip = '39.100.88.119'

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
    releasedate = models.CharField(max_length=1000 ,default="2015-01-15(中国大陆3D)", verbose_name='上映年份', null=True, blank=True)
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

    picture = models.CharField(max_length=1000, verbose_name='缩略图', null=True, blank=True,
                               default='/static/img/m16.jpg')
    # backpost = models.CharField(max_length=3000, verbose_name='详情页海报', null=True, blank=True,
                                # default='/static/img/m16.jpg')

    def __str__(self):
        return '%s - %s - %s - %s - %lf - %s' % (
        self.directors, self.moviename, self.nation, self.releasedate, self.averating, self.picture)

    class Meta:
        verbose_name = '电影信息'
        verbose_name_plural = verbose_name

# 电影相似度表
class MovieSimilar(models.Model):



    def getSimilar(self,movie_id):
        c = happybase.Connection(host=hbase_ip, port=9090)
        c.open()
        recommend_table = happybase.Table('movie_sim_1', c)
        tmp_dict = recommend_table.row(str(movie_id))
        movie_id_str = ''
        for key, value in tmp_dict.items():
            movie_id_str = value.decode('utf-8')
        movie_list = []
        if len(movie_id_str) > 0:
            movie_id_list = movie_id_str.split(',')
            for movie_id in movie_id_list:
                tmp = MovieInfo.objects.get(id=int(movie_id))
                movie_list.append(tmp)
        c.close()
        return movie_list
    # item1 = models.IntegerField(default=0, verbose_name='电影id')
    # item2 = models.IntegerField(default=0, verbose_name='电影id')
    #
    # similar = models.FloatField(default=0, verbose_name='相似度')
    #
    # def __str__(self):
    #     return '%d - %d - %lf' % (self.item1, self.item2, self.similar)
    #
    # class Meta:
    #     verbose_name = '电影相似度信息'
    #     verbose_name_plural = verbose_name

# 用户评论以及电影评分表
# 一条评论是属于一个用户对一个电影的，所以user和movie都是多对一，使用ForeignKey


class Review(models.Model):


    def revert(self, result):
        li = []
        if(len(result)>0):
            for i in range(0,len(result)):
                key = result[i][0]
                dic = result[i][1]
                key = key.decode('utf-8')
                Dic = {}
                for rowkey, value in dic.items():
                    tmp = (rowkey.decode('utf-8').split(':'))[1]
                    Dic[tmp] = value.decode('utf-8')
                tup = (key, Dic)
                li.append(tup)
            return li
        else:
            return None
    def revert_user(self, result):
        li = []
        if(len(result)>0):
            for i in range(0,len(result)):
                key = result[i][0]
                dic = result[i][1]
                key = key.decode('utf-8')
                Dic = {}
                for rowkey, value in dic.items():

                    tmp = (rowkey.decode('utf-8').split(':'))[1]
                    Dic[tmp] = value.decode('utf-8')
                Dic['user'] = UserProfile.objects.get(id = key.split('_')[0]).username
                tup = (key, Dic)
                li.append(tup)
            return li
        else:
            return None
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

# 需要全部转成utf-8

    def getComments_movie(self,movie_id):
        c = happybase.Connection(host=hbase_ip, port=9090)
        c.open()
        comment_table = happybase.Table('comment', c)
        query_str = "RowFilter (=, 'substring:_" + str(movie_id) + "')"
        query = comment_table.scan(filter=query_str, limit=1000)
        try:
            result = list(query)
        except:
            c.close()
            return []
        result = self.revert(result)
        c.close()
        return result[0:10]


    def getUserComments_movie(self,movie_id):
        c = happybase.Connection(host=hbase_ip, port=9090)
        c.open()
        comment_table = happybase.Table('comment_local', c)
        query_str = "RowFilter (=, 'substring:_" + str(movie_id) + "')"
        query = comment_table.scan(filter=query_str, limit=1000)
        try:
            result = list(query)
        except:
            c.close()
            return []
        result = self.revert_user(result)
        c.close()
        return result

    def getUserComment_user(self, user_id):
        c = happybase.Connection(host=hbase_ip, port=9090)
        c.open()
        comment_table = happybase.Table('comment_local', c)
        query_str = "RowFilter (=, 'substring:" + str(user_id) + "_')"
        query = comment_table.scan(filter=query_str, limit=1000)
        result = list(query)
        result = self.revert_user(result)
        c.close()
        return result

    def hasUserComment(self, movie_id, user_id):
        c = happybase.Connection(host=hbase_ip, port=9090)
        c.open()
        comment_table = happybase.Table('comment_local',c)
        query_str = "RowFilter (=, 'binary:" + str(user_id) + "_" + str(movie_id) + "')"
        query = comment_table.scan(filter=query_str, limit=1000)
        try:
            result = list(query)
        except:
            c.close()
            return False
        c.close()
        if len(result) == 0:
            return False
        else:
            return True


    def addUserComment(self,movie_id, user_id, content, star, reviewtime):
        c = happybase.Connection(host=hbase_ip, port=9090)
        c.open()
        comment_table = happybase.Table('comment_local', c)
        if self.hasUserComment(movie_id, user_id):
            c.close()
            return False
        comment_table.put(str(user_id) + "_" + str(movie_id), {"region:content": str(content),
                                                     "region:star": str(star),
                                                     "region:reviewtime":str(reviewtime)})
        c.close()

    def deleteUserComment(self, movie_id, user_id):
        c = happybase.Connection(host=hbase_ip, port=9090)
        c.open()
        comment_table = happybase.Table('comment_local', c)
        comment_table.delete(str(user_id)+ "_" + str(movie_id))
        c.close()


    def free(self):
        self.connection.close()


    # def __str__(self):
    #     return '%s - %s - %lf' % (self.user.username, self.movie.moviename, self.star)

    # class Meta:
    #     verbose_name = '用户打分及评论'
    #     verbose_name_plural = verbose_name


