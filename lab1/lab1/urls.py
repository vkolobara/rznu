"""lab1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_api import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view

user_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', get_swagger_view(title="Documentation")),
    url(r'^api/posts/$', views.PostList.as_view(), name='post-list'),
    url(r'^api/posts/(?P<pk>[0-9]+)$', views.PostDetail.as_view(), name='post-detail'),
    url(r'^api/posts/(?P<post>[0-9]+)/comments/$', views.CommentByPostList.as_view(), name='comment-by-post-list'),
    url(r'^api/comments/$', views.CommentList.as_view(), name='comment-list'),
    url(r'^api/comments/(?P<pk>[0-9]+)$', views.CommentDetail.as_view(), name='comment-detail'),
    url(r'^api/users/$', user_list, name='user-list'),
    url(r'^api/users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    url(r'^api/users/(?P<author>[0-9]+)/posts/$', views.PostByUserList.as_view(), name='post-by-user-list'),
    url(r'^api/users/(?P<author>[0-9]+)/comments/$', views.CommentByUserList.as_view(), name='comment-by-user-list'),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
