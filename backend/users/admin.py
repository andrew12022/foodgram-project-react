from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Subscriber

admin.site.register(User, UserAdmin)
admin.site.register(Subscriber)
