#!/usr/bin/env python
#coding: utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url('^user_command_list', views.user_command_list, name='command_list'),
    url('^user_command_manage/add', views.user_command_manage, name='commad_add'),
    url('^user_command_manage/delete', views.user_command_manage, name='commad_delete'),
    url('^user_perm/dir/$', views.user_dir_list, name='dir_list'),
]
