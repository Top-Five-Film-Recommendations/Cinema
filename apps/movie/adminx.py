import xadmin

from movie.models import MovieInfo, MovieSimilar,Review


class MovieInfoAdmin(object):
    # 列表默认显示
    list_display = ['id', 'moviename', 'releasedate', 'typelist', 'nation', 'directors', 'editors', 'leadactors','averating', 'numrating', 'picture']
    # 搜索范围
    search_fields = ['id']
    # 列表过滤
    list_filter = ['releasedate', 'typelist', 'nation']
    # 直接编辑
    list_editable = ['moviename', 'releasedate', 'typelist', 'nation', 'directors', 'editors', 'leadactors', 'picture']
    # 默认排序
    ordering = ['releasedate', 'moviename', 'typelist']




class MovieSimilarAdmin(object):
    list_display = ['id', 'item1', 'item2', 'similar']
    search_fields = ['id', 'item1', 'item2', 'similar']
    list_editable = ['id', 'item1', 'item2', 'similar']
    ordering = ['id', 'item1', 'item2', 'similar']


class ReviewAdmin(object):
    list_display = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']
    search_fields = ['id', 'user', 'movie', 'content', 'star']
    list_filter = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']
    list_editable = ['user', 'movie', 'content', 'star']
    ordering = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']


xadmin.site.register(MovieInfo, MovieInfoAdmin)
xadmin.site.register(Review, ReviewAdmin)
xadmin.site.register(MovieSimilar, MovieSimilarAdmin)

