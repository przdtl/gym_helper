from django.contrib import admin

from account.models import UserModel, EmailVerification


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    pass
