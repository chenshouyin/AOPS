# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class PackageTag(models.Model):
    package_name = models.CharField(max_length=30, verbose_name=u'包名')
    tag = models.IntegerField(unique=True, verbose_name=u'标签')
    md5 = models.CharField(max_length=10000, default='', verbose_name=u'标签')
