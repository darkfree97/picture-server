from django.contrib import admin
from . import models


@admin.register(models.RegularUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')

    @staticmethod
    def first_name(obj):
        return obj.profile.first_name

    @staticmethod
    def last_name(obj):
        return obj.profile.last_name


@admin.register(models.Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')

    @staticmethod
    def first_name(obj):
        return obj.profile.first_name

    @staticmethod
    def last_name(obj):
        return obj.profile.last_name


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(models.HashTag)
class HashTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
