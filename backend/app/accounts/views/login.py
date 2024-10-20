import time

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from app.accounts.models import User
from app.accounts.serializers import UserRegisterSerializer
from app.chatgpt.models import ChatgptAccount
from app.settings import ADMIN_USERNAME, FREE_ACCOUNT_USERNAME
from app.settings import CHATGPT_GATEWAY_URL
from app.utils import save_visit_log, req_gateway


class UserFreeLoginView(APIView):
    def post(self, request):
        user = User.objects.filter(username=FREE_ACCOUNT_USERNAME, is_active=True).first()
        if not user:
            raise ValidationError({"message": "当前系统无免费账号可用"})
        request.user = user

        token, created = Token.objects.get_or_create(user=user)
        save_visit_log(request, "login")

        return Response({'admin_token': token.key})


class AccountLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.last_login = timezone.now()
        user.save()


        token, created = Token.objects.get_or_create(user=user)
        request.user = user

        save_visit_log(request, "login")

        result = {'admin_token': token.key}
        if user.username == ADMIN_USERNAME:
            result.update({"is_admin": True})
        return Response(result)

class AccountRegister(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = CHATGPT_GATEWAY_URL + "/api/get-user-info"

        res_json = req_gateway("post", url, json={"chatgpt_token": serializer.data["chatgpt_token"]})
        chatgptaccount_id = ChatgptAccount.save_data(res_json)

        user = User.objects.filter(username=serializer.data["username"]).first()
        if user and not authenticate(username=serializer.data["username"], password=serializer.data["password"]):
            raise ValidationError({"message": "账号已存在"})

        # 创建默认号池
        from app.chatgpt.models import ChatgptCar
        chatgptcar, created = ChatgptCar.objects.get_or_create(car_name="reg_{}".format(serializer.data["username"]), defaults={
            "created_time":int(time.time()),
            "updated_time":int(time.time()),
            "remark": "用户注册时，系统自动创建"
        })
        gpt_account_list = list(chatgptcar.gpt_account_list)
        gpt_account_list.append(chatgptaccount_id)
        chatgptcar.gpt_account_list = list(set(gpt_account_list))
        chatgptcar.save()


        user, created = User.objects.get_or_create(username=serializer.data["username"])
        user.set_password(serializer.data["password"])
        user.last_login = timezone.now()
        gptcar_list = list(user.gptcar_list)
        gptcar_list.append(chatgptcar.id)
        user.gptcar_list = list(set(gptcar_list))
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({"admin_token": token.key})
