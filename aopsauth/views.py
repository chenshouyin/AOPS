#!/usr/bin/env python
#coding: utf-8

import re

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from .forms import UserForm
from aopsperm.models import PermLog
from .models import User, UserGroup


def index(request):
    '''分页功能
    '''
    all_users = User.objects.all()
    paginator = Paginator(all_users, 1)
    page = request.GET.get('page')
    try:
        user = paginator.page(page)
    except PageNotAnInteger:
        user = paginator.page(1)
    return render(request, 'aopsauth/index.html', {'user': user})


def login(request):
    '''
    登陆. 直接使用使用auth.forms 中自带的AuthenticationForm 类作为表单
    '''
    host_ip = "192.168.1.1"
    if request.user.is_authenticated():
        return redirect('user_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user and user.is_active:
                auth_login(request, user)       
                PermLog.objects.create(_type=u'用户登录', user=user, action=u'用户登录', action_ip=host_ip,
                        content=u'登录用户 {}'.format(user))
                return redirect('user_list')
            return HttpResponse('用户未激活')

        else:
            PermLog.objects.create(_type=u'用户登录', user=request.user, action=u'用户登录', action_ip=host_ip,
                        content=u'登录失败 {}'.format(request.user))
            return HttpResponse('数据验证失败')
    else:
        form  = AuthenticationForm()
    return render(request, 'aopsauth/login.html', {'form': form}) 


@login_required
def logout(request):
    '''
    退出当前用户并重定向至登陆站点
    '''
    auth_logout(request)
    return redirect('login')


@login_required
def group_list(request):
    groups = UserGroup.objects.all()
    return render(request, 'aopsauth/group_list.html', {'groups': groups})


@login_required
def user_list(request):
    all_users = User.objects.all()
    return render(request, 'aopsauth/user_list.html', {'all_users': all_users})


@login_required
def user_manage(request, action=None, uid=None):
    '''
    用户管理：增加 编辑 删除
    action: add edit delete
    '''
    if request.user.has_perm('edit_user'):
        if action == "add":
            if request.method == "POST":
                form = UserForm(request.POST)   #为什么这里写UserForm(request, request.POST) 就不能使用form.save()？
                if form.is_valid():
                    is_superuser = False
                    is_staff = False
                    is_active = False
                    username = request.POST.get('username')
                    first_name = request.POST.get('first_name')
                    last_name = request.POST.get('last_name')
                    password = request.POST.get('password')
                    email = request.POST.get('email')
                    mobile = request.POST.get('mobile')
                    role = request.POST.get('role')
                    user_permissions = request.POST.get('user_permissions')
                    group = request.POST.get('group')

                    if 'is_superuser' in request.POST:
                        is_superuser = True
                    if 'is_staff' in request.POST:
                        is_staff = True
                    if 'is_active' in request.POST:
                        is_active = True

                    #注意，此处使用create_user创建用户;直接提交表单只能将数据入库而认证系统并没有创建这个用户
                    user = User.objects.create_user(username=username,
                            first_name=first_name,
                            last_name=last_name,
                            password=password,
                            email=email,
                            mobile=mobile,
                            role=role,
                            is_superuser=is_superuser,
                            is_staff=is_staff,
                            is_active=is_active)
                    user.save()

                    #ValueError: "<User: gengyangyang>" needs to have a value for field "id" before 
                    #this many-to-many relationship can be used.
                    # 多对多关系不能直接放在create_user() 中，需要使用管理器添加。否则会出现上述错误
                    user.user_permissions.add(user_permissions)
                    user.group.add(group)
                    return redirect('user_list')
            else:
                form = UserForm()
                return render(request, 'aopsauth/user_add.html', {'form': form})

        if action == "edit":
            return HttpResponse('you can edit {}'.format(uid))

        if action == "delete":
            u = User.objects.get(pk=uid)
            u.delete()

            try:
                User.objects.get(id=uid)
            except:
                return redirect(user_list)
    else:
        return HttpResponse('you can not edit')
