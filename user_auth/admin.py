from django.contrib import admin
from user_auth.models import ExtraData, Gender
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class ExtraInline(admin.StackedInline):
    model = ExtraData


class UserAdminModified(UserAdmin):
    inlines = (ExtraInline,)


admin.site.register(Gender)
admin.site.unregister(User)
admin.site.register(User, UserAdminModified)
