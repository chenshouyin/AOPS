#!/usr/bin/env python
#coding: utf-8

from rest_framework import serializers
from .models import AssetGroup

class AssetGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetGroup
        fields = ('name', 'comment')
    '''
    def create(self, validated_data):
        return AssetGroup.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance
    '''


