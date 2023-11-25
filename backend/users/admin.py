from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Subscriber, User

admin.site.empty_value_display = 'Не задано'


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'email',
        'first_name',
    )


@admin.register(Subscriber)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
