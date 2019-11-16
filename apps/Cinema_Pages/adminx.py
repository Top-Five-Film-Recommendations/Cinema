import xadmin
from Cinema_Pages.models import DefaultRecom
#
# class ReviewAdmin(object):
#     list_display = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']
#     search_fields = ['id', 'user', 'movie', 'content', 'star']
#     list_filter = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']
#     list_editable = ['user', 'movie', 'content', 'star']
#     ordering = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']


class DefaultRecomAdmin(object):
    list_display = ['id', 'movie', 'redate']
    search_fields = ['id', 'movie']
    list_filter = ['id', 'movie', 'redate']
    ordering = ['id', 'movie', 'redate']

#
# class StaRecomAdmin(object):
#     list_display = ['id', 'user', 'movie']
#     search_fields = ['id', 'userid', 'movie']
#     list_filter = ['id', 'user', 'movie']
#     ordering = ['id', 'user', 'movie']


# xadmin.site.unregister(UserProfile)
# xadmin.site.register(UserProfile, UserProfileAdmin)

# xadmin.site.register(Review, ReviewAdmin)
xadmin.site.register(DefaultRecom, DefaultRecomAdmin)
# xadmin.site.register(StaRecom, StaRecomAdmin)



