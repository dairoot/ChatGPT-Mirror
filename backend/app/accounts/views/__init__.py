from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from app.accounts.models import User, VisitLog
from app.accounts.serializers import ShowVisitLogModelSerializer, AddUserAccountSerializer, UserBindChatGPTSerializer, \
    ShowUserAccountModelSerializer, BatchModelLimitSerializer
from app.chatgpt.models import ChatgptAccount, ChatgptCar
from app.page import DefaultPageNumberPagination
from app.settings import ADMIN_USERNAME
from app.utils import generate_md5


class UserChatGPTAccountList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        results = []
        chatgpt_account_list = []
        for line in ChatgptCar.objects.filter(id__in=request.user.gptcar_list).values("gpt_account_list"):
            chatgpt_account_list.extend(line["gpt_account_list"])

        gptaccount = ChatgptAccount.objects
        if chatgpt_account_list:
            gptaccount = gptaccount.filter(id__in=chatgpt_account_list)
        for line in gptaccount.all():
            results.append({
                "id": line.id,
                "chatgpt_flag": "{}{}".format(line.id,generate_md5(line.chatgpt_username)[:5]),
                "plan_type": line.plan_type
            })

        return Response({"results": results})


class BatchModelLimit(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        serializer = BatchModelLimitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.filter(id__in=serializer.data["user_id_list"]).update(model_limit=serializer.data["model_limit"])
        return Response({"message": "更新成功"})


class UserRelateGPTCarView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request, *args, **kwargs):
        serializer = UserBindChatGPTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for user_id in serializer.data["user_id_list"]:
            user = User.objects.filter(id=user_id).first()
            user.gptcar_list = serializer.data["gptcar_id_list"]
            user.save()

        return Response({"message": "绑定成功"})


class UserAccountView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = User.objects.order_by("-id").all()
    serializer_class = ShowUserAccountModelSerializer
    pagination_class = DefaultPageNumberPagination

    def post(self, request, *args, **kwargs):
        # 添加或更新用户
        serializer = AddUserAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.data["username"] == ADMIN_USERNAME:
            raise ValidationError({"message": "管理员账号不能操作"})

        user, created = User.objects.get_or_create(username=serializer.data["username"], defaults=serializer.data)

        if serializer.data.get("password"):
            user.set_password(serializer.data["password"])

        user.gptcar_list = serializer.data["gptcar_list"]
        user.is_active = serializer.data["is_active"]
        user.model_limit = serializer.data["model_limit"]
        user.isolated_session = serializer.data["isolated_session"]
        user.remark = serializer.data["remark"]
        user.save()

        return Response({"message": "添加成功"})

    def delete(self, request, *args, **kwargs):
        username = request.data.get("username")
        if username == ADMIN_USERNAME:
            raise ValidationError({"message": "不能删除管理员账号"})
        User.objects.filter(username=username).delete()
        return Response({"message": "删除成功"})


class VisitLogView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = VisitLog.objects.order_by("-id").all()
    serializer_class = ShowVisitLogModelSerializer
    pagination_class = DefaultPageNumberPagination
