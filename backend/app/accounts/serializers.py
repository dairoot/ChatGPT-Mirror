from rest_framework import serializers

from app.accounts.models import User, VisitLog
from app.chatgpt.models import ChatgptAccount


class ShowVisitLogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitLog
        fields = "__all__"


class ShowUserAccountModelSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    use_count = serializers.SerializerMethodField()
    chatgpt_count = serializers.SerializerMethodField()

    def __init__(self, *args, use_count_dict=dict, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_count_dict = use_count_dict

    def get_chatgpt_count(self, obj):
        return ChatgptAccount.get_by_gptcar_list(obj.gptcar_list).count()

    def get_use_count(self, obj):
        return self.use_count_dict.get(obj.username, 0)

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
    expired_date = serializers.DateField(required=False, allow_null=True)


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
