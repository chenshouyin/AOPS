#!/usr/bin/env python
#coding: utf-8

from django import forms
from .models import Asset, AssetGroup, IDC

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = "__all__"

class IDCForm(forms.ModelForm):
    class Meta:
        model = IDC
        fields = "__all__"

