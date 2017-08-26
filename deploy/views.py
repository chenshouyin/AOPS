#/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import time
import random

from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.shortcuts import redirect
from django.conf import settings

from .md5 import md5
from .saltlib import SaltAPI
from .forms import RomoteCMDForm, HostForm, FileUploadForm, FileDistriForm
from .models import PackageTag
from .supervisorlib import SuperVisor
from asset.models import Asset


UPLOAD_DIR = "/srv/salt/upload"
SALT_FileServer = "salt://upload"


# Create your views here.
@login_required
def index(request):
    value = random.randint(1, 100)
    return render(request, "deploy/index.html",  {'value': value})


@login_required
def remote_cmd(request):
    '''
    单个主机执行远程命令
    '''
    saltapi = SaltAPI('https://127.0.0.1:8000', username='saltapi', password='123456')

    if request.method == 'POST':
        form = RomoteCMDForm(request.POST)
        if form.is_valid():
            command = request.POST['command']
            target_host = request.POST['target_host']
            result = saltapi.remote_execution(target_host, command)
            return HttpResponse(result)
    else:
        form = RomoteCMDForm()
        return render(request, "deploy/remote_cmd.html", {'form': form})


@login_required
def file_upload(request):
    '''文件上传至AOPS服务器/srv/salt/upload 目录
    '''
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            _file = request.FILES['_file']
            #target_host = request.POST['target_host']
        
            filename = _file.name
            local_path = os.path.join(UPLOAD_DIR, filename)
            
            #上传的文件写入到服务器
            with open(local_path, 'wb+') as f:
                for chunk in _file.chunks():
                    f.write(chunk)

            timestamp = int(time.time())
            _md5 = md5(local_path)
            packagetag = PackageTag(package_name=filename, tag = timestamp, md5=_md5)
            packagetag.save()
            return redirect('file_upload')
    else:
        form = FileUploadForm()
        return render(request, "deploy/file_upload.html", {'form': form})

@login_required
def file_distribute(request):
    '''将upload 中的文件 文件分发至minion
    '''
    if request.method == 'POST':
        form = FileDistriForm(request.POST)
        if form.is_valid():
            filename = request.POST['filename']
            target_host = request.POST['target_host']
            remote_path = os.path.join(request.POST['remote_dir'], filename)

            saltapi = SaltAPI('https://127.0.0.1:8000', username='saltapi', password='123456')
            result = saltapi.file_distribute(target_host, arg=["{}/{}".format(SALT_FileServer ,filename),remote_path])
            if result:
                messages.add_message(request, messages.SUCCESS, 'sucess')
            else:
                messages.add_message(request, messages.ERROR, u'ERROR: 文件分发失败')
            return redirect('file_distribute')
    else:
        form = FileDistriForm()
        return render(request, "deploy/file_distribute.html", {'form': form})


@login_required
def supervisor(request):
    '''展示所有主机的进程。目前没有判断哪些主机使用了supervisor.需要做判断
    '''
    all_process_info = {}
    hostinfo = [(host.hostname, host.ip) for host in Asset.objects.all()]
    port = 9001
    for info in hostinfo:
        hostname, ip = info
        visor = SuperVisor(ip, port)
        all_process_info[hostname] = visor.getAllProcessInfo()
    
    return render(request, 'deploy/supervisor.html', {'all_process_info': all_process_info})


@login_required
def su_manage(request, hostname=None, processname=None):
    '''管理进程。
    '''

    ip = ''
    port = 9001
    hostinfo = [(host.hostname, host.ip) for host in Asset.objects.all()]
    for info in hostinfo:
        if hostname in info:
            ip = info[1]
    print processname
    print (port, ip)
    visor = SuperVisor(ip, port)
    if request.method == "POST":
        '''
        if request.POST.get('restart'):
            visor.stopProcess(processname)
            visor.startProcess(processname)
            return redirect('supervisor')
        '''

        if request.POST.get('start'):
            visor.startProcess(processname)
            return redirect('supervisor')

        else:
            visor.stopProcess(processname)
            return redirect('supervisor')
    else:
        return redirect('supervisor')


