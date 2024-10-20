# -*- coding: utf-8 -*-
from django.contrib import admin

from app.chatgpt.models import ChatgptAccount, ChatgptCar


@admin.register(ChatgptAccount)
class ChatgptTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "chatgpt_username",
        "plan_type",
        "remark",
    )


@admin.register(ChatgptCar)
class ChatgptTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "car_name",
        "gpt_account_list",
    )
