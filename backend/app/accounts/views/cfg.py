from rest_framework.response import Response
from rest_framework.views import APIView

from app.settings import SHOW_GITHUB


class VersionConfig(APIView):

    def get(self, request):
        return Response({'show_github': SHOW_GITHUB})
