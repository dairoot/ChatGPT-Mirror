from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from app.chatgpt.models import ChatgptCar
from app.chatgpt.serializers import ShowGptCarSerializer, AddChatgptCarModelSerializer, DeleteChatgptCarSerializer
from app.page import DefaultPageNumberPagination


class GptCarEnum(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        result = ChatgptCar.objects.order_by("-id").values("id", "car_name").all()
        return Response({"data": result})


class GptCarView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = ChatgptCar.objects.order_by("-id").all()
    serializer_class = ShowGptCarSerializer
    pagination_class = DefaultPageNumberPagination

    def post(self, request, *args, **kwargs):
        obj = ChatgptCar.objects.filter(id=request.data.get("id")).first()
        serializer = AddChatgptCarModelSerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        serializer = DeleteChatgptCarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ChatgptCar.objects.filter(id__in=serializer.data["ids"]).delete()
        return Response({"message": "删除成功"})
