from rest_framework import serializers

from app.chatgpt.models import ChatgptAccount, ChatgptCar
import jwt
from app.utils import clean_int_list
import time

class ShowGptCarSerializer(serializers.ModelSerializer):
    gpt_account_name_list = serializers.SerializerMethodField()

    def get_gpt_account_name_list(self, obj):
        gpt_account_list = clean_int_list(obj.gpt_account_list)
        resutls = ChatgptAccount.objects.filter(id__in=gpt_account_list).values_list("chatgpt_username")
        return [i[0] for i in resutls]

    class Meta:
        model = ChatgptCar
        fields = "__all__"

class AddChatgptCarModelSerializer(serializers.ModelSerializer):

    def validate_empty_values(self, data):
        if not self.instance:
            data["created_time"] = int(time.time())

        data["updated_time"] = int(time.time())
        return (False, data)

    class Meta:
        model = ChatgptCar
        fields = "__all__"

class DeleteChatgptCarSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())


class ShowChatgptTokenSerializer(serializers.ModelSerializer):
    access_token_exp = serializers.SerializerMethodField()
    use_count = serializers.SerializerMethodField()

    def __init__(self, *args, use_count_dict=dict, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_count_dict = use_count_dict

    def get_use_count(self, obj):
        return self.use_count_dict.get(obj.chatgpt_username, 0)

    def get_access_token_exp(self, obj):
        try:
            access_token_exp = jwt.decode(obj.access_token, options={"verify_signature": False})["exp"]
        except Exception:
            access_token_exp = 0
        return access_token_exp

    class Meta:
        model = ChatgptAccount
        fields = "__all__"


class AddChatgptTokenSerializer(serializers.Serializer):
    chatgpt_token_list = serializers.ListField(child=serializers.CharField(allow_blank=True))

class DeleteChatgptAccountSerializer(serializers.Serializer):
    chatgpt_username = serializers.CharField()

class UpdateChatgptInfoSerializer(serializers.Serializer):
    chatgpt_username = serializers.CharField()
    remark = serializers.CharField()


class ChatGPTLoginSerializer(serializers.Serializer):
    chatgpt_id = serializers.IntegerField()
