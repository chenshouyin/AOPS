from django.contrib import admin
from .models import User, UserGroup
# Register your models here.

admin.site.register(User)
admin.site.register(UserGroup)
