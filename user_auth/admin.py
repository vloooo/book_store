from django.contrib import admin
from user_auth.models import ExtraData
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# class for attaching some model to another in django.admin
class ExtraInline(admin.TabularInline):
    model = ExtraData
    verbose_name_plural = 'ExtraData'


# new view manager user model for django.admin
class UserAdminModified(UserAdmin):
    inlines = (ExtraInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdminModified)
