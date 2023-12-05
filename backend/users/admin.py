from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Subscriber, User

admin.site.empty_value_display = 'Не задано'


@admin.register(User)
class UserAdmin(UserAdmin):
    """Админ модель для пользователя."""
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'count_of_recipes',
        'count_of_subscribers',
    )
    list_filter = (
        'email',
        'first_name',
    )

    def count_of_recipes(self, object):
        return object.recipes.count()
    count_of_recipes.short_description = 'Количество рецептов'

    def count_of_subscribers(self, object):
        return object.author_subscribers.count()
    count_of_subscribers.short_description = 'Количество подписчиков'


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Админ модель для подписчика."""
    list_display = (
        'user',
        'author',
    )
