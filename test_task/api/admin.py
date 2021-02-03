from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as UserAuth
from .models import *


class Users(admin.ModelAdmin):
    model = User


class Categories(admin.ModelAdmin):
    list_display = ('name', 'slug')


class Tags(admin.ModelAdmin):
    list_display = ('name', 'slug')


class Blogs(admin.ModelAdmin):
    list_display = ('title', 'content', 'creation_date', 'slug')
    filter_horizontal = ('tags',)


class Comments(admin.ModelAdmin):
    list_display = ('comment',)


admin.site.register(User, Users)
admin.site.register(Category, Categories)
admin.site.register(Tag, Tags)
admin.site.register(Blog, Blogs)
admin.site.register(Comment, Comments)
