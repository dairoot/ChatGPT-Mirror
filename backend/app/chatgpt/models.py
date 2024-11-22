import time

from django.db import models


class ChatgptCar(models.Model):
    car_name = models.CharField(unique=True, max_length=32)
    remark = models.CharField(max_length=128, blank=True, verbose_name="备注")
    gpt_account_list = models.JSONField(default=list)
    created_time = models.IntegerField(db_index=True, blank=True, verbose_name="创建时间")
    updated_time = models.IntegerField(db_index=True, blank=True, verbose_name="最后修改时间")

class ChatgptAccount(models.Model):
    chatgpt_username = models.CharField(max_length=64, unique=True)
    auth_status = models.BooleanField(default=True, verbose_name="授权状态")
    plan_type = models.CharField(max_length=32)
    access_token = models.TextField()
    session_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True,verbose_name="备注")
    created_time = models.IntegerField(db_index=True, blank=True, verbose_name="创建时间")
    updated_time = models.IntegerField(db_index=True, blank=True, verbose_name="最后修改时间")

    @classmethod
    def get_by_gptcar_list(cls, gptcar_list):
        chatgpt_account_list = []
        for line in ChatgptCar.objects.filter(id__in=gptcar_list).values("gpt_account_list"):
            chatgpt_account_list.extend(line["gpt_account_list"])

        gptaccount = ChatgptAccount.objects
        if gptcar_list:
            gptaccount = gptaccount.filter(id__in=chatgpt_account_list)

        return gptaccount.order_by("-plan_type", "-id").all()


    @classmethod
    def get_by_id(cls, chatgpt_id):
        return cls.objects.filter(id=chatgpt_id).first()

    @classmethod
    def save_data(cls, data):
        obj = cls.objects.filter(chatgpt_username=data["user_info"]["email"]).first()
        new_obj = obj or cls()
        new_obj.chatgpt_username = data["user_info"]["email"]
        new_obj.plan_type = data["user_info"]["plan_type"]
        new_obj.access_token = data["access_token"]

        if data.get("auth_status") is not None:
            new_obj.auth_status = data["auth_status"]

        if data.get("session_token"):
            new_obj.session_token = data["session_token"]
            new_obj.refresh_token = None

        if data.get("refresh_token"):
            new_obj.refresh_token = data["refresh_token"]
            new_obj.session_token = None


        new_obj.updated_time = int(time.time())

        if not obj:
            new_obj.created_time = int(time.time())

        new_obj.save()
        return new_obj.id
