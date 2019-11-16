"""Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include, re_path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('Cinema_Pages.urls')),
# ]


import xadmin
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.conf.urls import url
from Cinema_Pages.views import Cinema_Pages_view, index, reCal_spark, movie_type, calDefaultRecom, ucf_recom
from user.views import LoginView, LogoutView,RegisterView
from movie.views import ContentView, AddReview,DeleteReview
from search.views import movie_search


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # 首页
    re_path(r'^$|^index$',index, name='index'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('movie_display/', Cinema_Pages_view.as_view(), name="movie_display",),
    path('register/', RegisterView.as_view(), name="register",),
    path('movieinfo/<int:movie_id>', ContentView.as_view(), name='movieinfo'),
    path('add_comment/', AddReview.as_view(), name='add_review'),
    path('index.html/~', reCal_spark, name='reCal_spark'),
    path('movie_display.html/~', calDefaultRecom, name='reCal_coldstart'),
    re_path(r'^movie/type/(?P<type>[\w]+)/', movie_type, name='movie_type'),
    re_path(r'^movie/search/', movie_search, name='movie_search'),
    path('delete_comment/', DeleteReview.as_view(), name='deletereview'),
    re_path(r'^movie/ucf',ucf_recom , name='ucf')
]
