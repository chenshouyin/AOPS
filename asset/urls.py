#!/usr/bin/env python
#coding: utf-8

from django.conf.urls import url
from . import views

from rest_framework.urlpatterns import format_suffix_patterns
from asset.models import Asset
from rest_framework import routers, serializers, viewsets



urlpatterns = [
    url(r'^$', views.index),
    url('^yantao', views.yantao),
    url(r'group_list', views.GroupList.as_view()),
    url(r'group/$', views.asset_group_list, name="group"),
    url(r'asset_group_detail/(?P<pk>[0-9]+)/$', views.asset_group_detail),
    url(r'^index', views.index, name="show_asset"),
    url(r'^add_asset', views.add_asset, name="add_asset"),
    url(r'^delete_asset/(?P<id>[0-9]+)', views.delete_asset, name="delete_asset"),
    url(r'^add_idc', views.add_idc, name="add_idc"),
    url(r'^show_idc', views.show_idc, name="show_idc"),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
