#!/usr/bin/env python
#coding: utf-8

from django import forms
from asset.models import Asset

import os 

UPLOAD_DIR = "/srv/salt/upload"

HOST_CHOICES = [(host.hostname, host.hostname) for host in Asset.objects.all()]

def getFile():
    if os.path.exists(UPLOAD_DIR):
        FILE_CHOICES = [(filename, filename) for filename in os.listdir(UPLOAD_DIR)]
    else:
        os.mkdir(UPLOAD_DIR)
        FILE_CHOICES = [(filename, filename) for filename in os.listdir(UPLOAD_DIR)]
    return FILE_CHOICES

class HostForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['hostname']

class RomoteCMDForm(forms.Form):
    target_host = forms.ChoiceField(label=u'目标主机', choices=HOST_CHOICES)
    command = forms.CharField(label=u'命令')

class FileUploadForm(forms.Form):
    _file = forms.FileField(label=u'文件')
    #target_host = forms.ChoiceField(label=u'主机列表', choices=HOST_CHOICES)

class FileDistriForm(forms.Form):
    FILE_CHOICES = getFile()
    filename = forms.ChoiceField(label=u'选择文件', choices=FILE_CHOICES)
    target_host = forms.ChoiceField(label=u'主机列表', choices=HOST_CHOICES)
    remote_dir = forms.CharField(label=u'远程路径')
