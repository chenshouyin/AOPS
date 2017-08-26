# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from aopsauth.models import UserGroup, User

ASSET_STATUS = (
    (1, u"运行"),
    (2, u"关机"),
    (3, u'维修'),
    (4, u"下架")
    )

class AssetGroup(models.Model):
    '''
    主机组
    '''
    name = models.CharField(max_length=80, unique=True)
    comment = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return self.name

class IDC(models.Model):
    '''
    机房信息
    '''
    name = models.CharField(max_length=32, verbose_name=u'机房名称')
    linkman = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name=u'联系人')
    phone = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name=u'联系电话')
    address = models.CharField(max_length=128, blank=True, null=True, default='', verbose_name=u"机房地址")
    network = models.TextField(blank=True, null=True, default='', verbose_name=u"IP地址段")
    operator = models.CharField(max_length=32, blank=True, default='', null=True, verbose_name=u"运营商")
    comment = models.CharField(max_length=128, blank=True, default='', null=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'IDC'
        verbose_name_plural = verbose_name

class Asset(models.Model):
    '''
    主机信息
    '''
    ip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"主机IP")
    other_ip = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"其他IP")
    hostname = models.CharField(unique=True, max_length=128, verbose_name=u'主机名')
    groups = models.ManyToManyField(AssetGroup, blank=True, verbose_name=u'所属主机组')
    idc = models.ForeignKey(IDC, blank=True, null=True,  on_delete=models.SET_NULL, verbose_name=u'机房')   #多对一。多个主机属于一个机房
    brand = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'硬件厂商型号')
    cpu = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'CPU')
    memory = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'内存')
    disk = models.CharField(max_length=1024, blank=True, null=True, verbose_name=u'硬盘')
    system_type = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"系统类型")
    status = models.IntegerField(choices=ASSET_STATUS, blank=True, null=True, default=1, verbose_name=u"机器状态")
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"SN码")
    date_added = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=u"是否激活")
    comment = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.ip















 

