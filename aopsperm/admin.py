#!/usr/bin/env python
#coding: utf-8

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(PermLog)
admin.site.register(Command)
