#!/usr/bin/env python
#coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser, Permission


class UserGroup(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name=u'用户组')
    comment = models.TextField(blank=True, null=True, verbose_name=u'备注')
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=u'用户组权限',
        blank=True,
    )

    def __unicode__(self):
        return self.name

    class Meta:
        default_permissions = ()
        verbose_name = u'用户组'
        verbose_name_plural = u'用户组管理'

class User(AbstractUser):
    '''
    User 类 继承AbstractUser，因此自定义User与认证系统的Permission 依然是多对多关系，与Group也是多对多关系.
    因为自己定义了用户组，因此直接使用自定义的UserGroup和自定义User之间的多对多关系。 与认证系统默认的Group关系不需要使用
    '''
    USER_ROLE_CHOICES = (
        ('SU', u'超级管理员'),
        ('GA', u'组管理员'),
        ('CU', u'普通用户'),
    )
    mobile = models.CharField(max_length=30, blank=True, verbose_name=u'联系电话')
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='CU')
    group = models.ManyToManyField(UserGroup, related_name="user_group_set", verbose_name=u'用户属组')
    
    
    def __unicode__(self):
        return self.username

    class Meta:
        default_permissions = ()
        permissions = (
            ('view_user', u'查看用户'),
            ('edit_user', u'管理用户'),
        )

        verbose_name = u'用户'
        verbose_name_plural = u'用户管理'

class AdminGroup(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(UserGroup)

    def __unicode__(self):
        return '{}: {}'.format(self.user.username, self.group.name)

    class Meta:
        default_permissions = ()
        verbose_name = u'管理员组'
        verbose_name_plural = u'管理员组管理'
