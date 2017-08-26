#!/usr/bin/env python
#coding:utf-8

from django.conf.urls import url
from . import views 

urlpatterns = [
    url('^$', views.index, name="index"),
    url('^remote_cmd', views.remote_cmd, name='remote_cmd'),
    url('^file_upload', views.file_upload, name='file_upload'),
    url('^file_distribute', views.file_distribute, name='file_distribute'),
    #url('file_distribute', views.file_distribute, name='file_distribute'),
    url('^supervisor', views.supervisor, name="supervisor"),
    url('^su_manage/(?P<hostname>[a-zA-Z0-9_]+)/(?P<processname>[a-z0-9]+)', views.su_manage, name="su_manage"),
]
