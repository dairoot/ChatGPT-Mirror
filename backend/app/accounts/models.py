from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models
from app.chatgpt.models import ChatgptAccount


class User(AbstractUser):
    model_limit = models.JSONField(default=list, verbose_name="备注")
    remark = models.TextField(blank=True, verbose_name="备注")
    isolated_session = models.BooleanField(default=True, verbose_name="独立回话")
    gptcar_list = models.JSONField(default=list)
    expired_date = models.DateField(blank=True, null=True, verbose_name="过期日期")


class VisitLog(models.Model):
    # user = models.ForeignKey(User, db_constraint=False, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=150, verbose_name="用户名")
    chatgpt_username = models.CharField(max_length=150, null=True, verbose_name="chatgpt")
    log_type = models.CharField(max_length=20, verbose_name="登录类型")
    created_at = models.IntegerField(verbose_name="登录时间")
    ip = models.GenericIPAddressField(verbose_name="登录IP")
    user_agent = models.TextField(verbose_name="User-Agent")

    @classmethod
    def save_data(cls, data):
        obj = cls.objects.create(**data)
        return obj
