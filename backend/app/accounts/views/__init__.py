from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from app.accounts.models import User, VisitLog
from app.accounts.serializers import ShowVisitLogModelSerializer, AddUserAccountSerializer, UserBindChatGPTSerializer, \
    ShowUserAccountModelSerializer, BatchModelLimitSerializer
from app.chatgpt.models import ChatgptAccount
from app.page import DefaultPageNumberPagination
from app.settings import ADMIN_USERNAME
from app.utils import req_gateway


class GetMirrorToken(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.filter(id=request.GET["user_id"]).first()

        user_account_list = ChatgptAccount.get_by_gptcar_list(user.gptcar_list)
        chatgpt_username_list = [i.chatgpt_username for i in user_account_list]
        res = req_gateway("post", "/api/get-mirror-token", json={
            "isolated_session": user.isolated_session,
            "limits": user.model_limit,
            "chatgpt_list": chatgpt_username_list,
            "user_name": user.username,
        })
        for line in res:
            obj = ChatgptAccount.objects.filter(chatgpt_username=line["chatgpt_username"]).first()
            line["auth_status"] = obj.auth_status
        return Response(res)


class UserChatGPTAccountList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        results = []
        user_account_list = ChatgptAccount.get_by_gptcar_list(request.user.gptcar_list)
        for line in user_account_list:
            results.append({
                "id": line.id,
                "chatgpt_flag": "{:03}{}".format(line.id, line.chatgpt_username[:3]),
                "plan_type": line.plan_type,
                "auth_status": line.auth_status,
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

    def get(self, request, *args, **kwargs):
        queryset = User.objects.order_by("-id").all()
        pg = DefaultPageNumberPagination()
        pg.page_size_query_param = "page_size"
        page_accounts = pg.paginate_queryset(queryset, request=request)
        username_list = [i.username for i in page_accounts]
        try:
            use_count_dict = req_gateway("post", "/api/get-user-use-count", json={"username_list": username_list})
        except:
            use_count_dict = {}
        serializer = ShowUserAccountModelSerializer(instance=page_accounts, use_count_dict=use_count_dict, many=True)
        return pg.get_paginated_response(serializer.data)

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
