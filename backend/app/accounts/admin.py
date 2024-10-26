# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework.authtoken.models import TokenProxy

from app.accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_active",
        "username",
        "isolated_session",
        "remark",
        "last_login",
    )
    exclude = (
        # "password",
        "user_permissions",
        "last_name",
        "last_login",
        "is_staff",
        "is_superuser",
        "date_joined",
        "email",
        "groups",
    )


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
admin.site.site_header = "ChatGPT"
admin.site.site_title = "ChatGPT"
