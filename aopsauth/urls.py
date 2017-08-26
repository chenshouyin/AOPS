#!/usr/bin/env python
#coding: utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.index),
    url('^login', views.login, name='login'),
    url('^logout', views.logout, name='logout'),
    url('^user_list', views.user_list, name='user_list'),
    url('^user_manage/(?P<action>[a-z]+)/$', views.user_manage, name='user_add'),
    url('^user_manage/(?P<uid>\d+)/(?P<action>[a-z]+)/$', views.user_manage, name='user_edit'),
    url('^user_manage/(?P<uid>\d+)/(?P<action>[a-z]+)/$', views.user_manage, name='user_delete'),
    url('^group_list', views.group_list, name='group_list')
]
