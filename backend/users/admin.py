from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username', 'id', 'email', 'first_name', 'last_name',)
    list_filter = ('email',)
    empty_value_display = 'нет пользователей'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    empty_value_display = 'нет подписок'
