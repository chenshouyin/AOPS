#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
#from django.http import JsonResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


from .forms import AssetForm
from .forms import IDCForm
from .models import Asset
from .models import IDC
from .models import AssetGroup
from .serializers import AssetGroupSerializer


class GroupList(generics.ListCreateAPIView):
    '''使用基于类的视图编写 API视图
    '''    

    queryset = AssetGroup.objects.all()
    serializer_class = AssetGroupSerializer
        

@api_view(['GET', 'POST'])
@csrf_exempt
def asset_group_list(request, format=None):
    '''使用基于函数的视图编写 API视图
    查询资产组
    '''

    if request.method == 'GET':
        group = AssetGroup.objects.all()
        serializer = AssetGroupSerializer(group, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = AssetGroupSerializer(data=request.data)
        print serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def asset_group_detail(request, pk, format=None):
    try:
        group = AssetGroup.objects.get(pk=1)
    except AssetGroup.DoseNotExits:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AssetGroupSerializer(group)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AssetGroupSerializer(group, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        group.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@login_required
def yantao(request):
    return render(request, 'asset/asset_group_list.html')

@login_required
def index(request):
    '''show_asset
    '''
    asset_list = Asset.objects.values()
    paginator = Paginator(asset_list, 2)
    page = request.GET.get('page')
    try:
        asset = paginator.page(page)
    except PageNotAnInteger:
        asset = paginator.page(1)
    except EmptyPage:
        asset = paginator.page(paginator.num_pages)
    return render(request, 'asset/index.html', {'asset': asset})


@login_required
def add_asset(request):
    '''增加主机
    '''
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_asset')
            #return HttpResponse("test")
    else:
        form = AssetForm()
        return render(request, 'asset/add_asset.html', {'form': form})


@login_required
def delete_asset(request, id=None):
    '''删除主机
    '''
    host = Asset.objects.get(pk=id)
    host.delete()
    return redirect('show_asset')


@login_required
def show_idc(request):
    '''展示idc信息
    idc_list = IDC.objects.values()
    paginator = Paginator(idc, 2)

    page = request.GET.get('page')    
    try:
        idc = paginator.page(page)    
    except PageNotAnInteger:
        idc = paginator.page(1)
    '''
    idc = IDC.objects.values()
    return render(request, 'asset/show_idc.html', {'idc': idc})


@login_required
def add_idc(request):
    '''增加IDC信息
    '''
    if request.method == 'POST':
        form = IDCForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show_idc")
    else:
        form = IDCForm()
        return  render(request, 'asset/add_idc.html', {'form': form})            
