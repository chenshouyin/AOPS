#!/usr/bin/env python
#coding: utf-8

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


# Create your views here.

def UserIP(request):
    '''
    获取用户IP
    '''
    ip = request.META['REMOTE_ADDR']
    return ip

@login_required
def index(request):
    return render(request, 'userperm/index.html', {'value': range(20)}, {'lists': [2,3,4]})
    #return HttpResponse(request.user)
    #return render(request, 'userperm/base.html', {})

@login_required
def user_command_list(request):
    '''
    列出所有命令。这个功能暂还没什么实际作用。猜测作者之前是为了管理每个用户可以使用的命令的。
    url: name='command_list'
    '''

    if request.user.is_superuser:   
        command_list = UserCommand.objects.all()
        #return render(request, 'userperm/userperm_command_list.html', {'all_command': command_list})    
        return render(request, 'userperm/list.html', {'command_list': command_list}) 
    else:
        return Http404


@login_required
def user_command_manage(request, id=None):
    '''
    管理命令：增加、删除、编辑
    user_perm/exec/manage/add/
    user_perm/exec/manage/delete/
    user_perm/exec/manage/(?P<id>\d+)/edit/

    以add, delete, edit操作通过GET 方式 传入视图，视图进行判断决定行为
    '''
    if request.user.is_superuser:
        action = ''
        page_name = ''
        print request.GET
        if id:  #url中捕获的参数。id是正则表达式分组名为id
            command = get_object_or_404(UserCommand, pk=id)
            action = 'edit'
            page_name = '编辑命令'
        else:
            # http://139.199.160.32/userperm/user_command_manage/add
            command = UserCommand()
            action = 'add'
            page_name = '新增命令'

        if request.method == 'GET':
            if request.GET.has_key('delete'):   #dict.has_key(key) 判断字典是否含有某个key
                id = request.GET.get('id')
                command = get_object_or_404(UserCommand, pk=id)
                command.delete()
                
                Message.objects.create(_type=u'权限控制',
                    user=request.user.first_name,
                    action = u'删除命令',
                    action_ip=UserIP(request),
                    content=u'删除命令 %s' % command.name
                )               
                return redirect('command_list')
        
        if request.method == 'POST':
            form = CommandForm(request.POST, instance=command)
            if form.is_valid():
                if action == 'add':
                    command = form.save(commit=False)
                else:
                    form.save()
                command.save()
                Message.objects.create(_type=u'权限控制', 
                    user=request.user.first_name, 
                    action=page_name, 
                    action_ip=UserIP(request),
                    content='%s %s' % (page_name,command.name)
                )
                return redirect('command_list')
        else:
            form = CommandForm(instance=command)
        return render(request, 'userperm/userperm_command_manage.html',
                    {'form': form,
                    'action': action, 
                    'page_name': page_name
                })
    else:
        raise Http404

@login_required
def user_dir_list(request):
    if request.user.is_superuser:
        dir_list = UserDirectory.objects.all()
        return render(request, 'userperm/userperm_directory_list.html',
                      {'all_dir': dir_list})
    else:
        raise Http404


@login_required
def user_dir_manage(request, id=None):
    '''
    user_perm/dir/manage/add/
    user_perm/dir/manage/delete/
    user_perm/dir/manage/(?P<id>\d+)/edit/$
    '''

    if request.user.is_superuser:
        action = ''
        page_name = ''
        if id:
            directory = get_object_or_404(UserDirectory, pk=id)
            action = 'edit'
            page_name = '编辑目录'
        else:
            directory = UserDirectory()
            action = 'add'
            page_name = '新增目录'

    if request.method == 'GET':
        if request.GET.has_key('delete'):
            id = request.GET.get('id')
            directory = get_object_or_404(UserDirectory, pk=id)
            directory.delete()

            Message.objects.create(type=u'权限控制',
                user=request.user.first_name, 
                action=u'删除目录', 
                action_ip=UserIP(request),
                content=u'删除目录 %s' % directory.name
            )

            return redirect('dir_list')

        if request.method == 'POST':
            form = DirectoryForm(request.POST, instance=directory)
            if form.is_valid():
                if action == 'add':
                    directory = form.save(commit=False)
                else:
                    form.save()
                directory.save()
                Message.objects.create(type=u'权限控制', 
                    user=request.user.first_name, 
                    action=page_name, 
                    action_ip=UserIP(request),
                    content='%s %s' % (page_name,directory.name)
                )
                return redirect('dir_list')
        else:
            form = DirectoryForm(instance=directory)
        return render(request, 'userperm_directory_manage.html', {
                    'form': form, 'action': action, 'page_name': page_name})
    else:
        raise Http404

@login_required
def user_dir_list(request):
    '''
    user_perm/dir/
    '''
    if request.user.is_superuser:
        dir_list = UserDirectory.objects.all()
        return render(request, 'userperm/userperm_directory_list.html',
                    {'all_dir': dir_list})
    else:
        return Http404


