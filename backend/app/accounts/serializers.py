from rest_framework import serializers

from app.accounts.models import User, VisitLog


class ShowVisitLogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitLog
        fields = "__all__"


class ShowUserAccountModelSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = User
        exclude = (
            "password", "is_superuser", "first_name", "last_name", "email", "is_staff", "groups", "user_permissions")
        # fields = "__all__"


class AddUserAccountSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField()
    username = serializers.CharField(min_length=4)
    password = serializers.CharField(required=False)
    gptcar_list = serializers.JSONField(default=list)
    model_limit = serializers.JSONField(default=dict)
    remark = serializers.CharField(default="", allow_blank=True)
    isolated_session = serializers.BooleanField()


class BatchModelLimitSerializer(serializers.Serializer):
    user_id_list = serializers.ListField(child=serializers.IntegerField())
    model_limit = serializers.JSONField()


class UserBindChatGPTSerializer(serializers.Serializer):
    user_id_list = serializers.ListField(child=serializers.IntegerField())
    gptcar_id_list = serializers.ListField(child=serializers.IntegerField())


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4)
    password = serializers.CharField()
    chatgpt_token = serializers.CharField()
