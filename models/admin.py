from django.contrib import admin
from .models import UserModel, ComeGoneTimeModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'status']
    list_filter = ['status', 'full_name']



@admin.register(ComeGoneTimeModel)
class ComeGOneTimeAdmin(admin.ModelAdmin):
    list_display = ['user', 'time', 'status']
    list_filter = [ 'status', 'user']