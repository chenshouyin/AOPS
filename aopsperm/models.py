#!/usr/bin/env python
#coding: utf-8

from __future__ import unicode_literals

from django.db import models
from aopsauth.models import UserGroup, User
from asset.models import AssetGroup, Asset


# Create your models here.
class PermLog(models.Model):
    '''记录用户操作
    '''
    user = models.CharField(max_length=244, verbose_name=u'用户')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    _type = models.CharField(max_length=10, verbose_name=u'类型')
    action = models.CharField(max_length=20, verbose_name=u'动作')
    action_ip = models.CharField(max_length=15, verbose_name=u'用户IP')
    content = models.TextField(verbose_name=u'内容')

    class Meta:
        default_permissions = ()
        permissions = (
            ('view_message', u'查看操作记录'),
            ('edit_message', u'管理操作记录'),
        )
        ordering = ['-datetime']
        verbose_name = u'审计信息'
        verbose_name_plural = u'审计信息管理'

class Command(models.Model):
    '''
    远程命令定义
    用户和远程命令是多对多关系
    用户组和远程命令是多对多关系
    is_allow 定义是否拥有该命令权限
    用户对命令的权限有: add change delete
    '''
    name = models.CharField(max_length=80, unique=True, verbose_name=u'命令组')
    command = models.TextField(blank=True, verbose_name=u'系统命令')
    user_group = models.ManyToManyField(UserGroup, related_name='perm_rule')
    user = models.ManyToManyField(User, related_name='perm_rule')
    is_allow = models.BooleanField(default=True, verbose_name=u'状态')
    
    def __str__(self):
        return self.name
    
