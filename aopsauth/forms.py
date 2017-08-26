#!/usr/bin/env python
#coding: utf-8

from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        #fields = ['username', 'password']
        #fields = '__all__'
        fields = [
                'username',
                'first_name',
                'last_name',
                'password', 
                'email',
                'is_superuser',
                'is_staff',
                'is_active',
                'mobile',
                'role',
                'user_permissions',
                'group',
                ]

