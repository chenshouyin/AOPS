# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import AssetGroup, IDC, Asset

# Register your models here.
admin.site.register(AssetGroup)
admin.site.register(IDC)
admin.site.register(Asset)
