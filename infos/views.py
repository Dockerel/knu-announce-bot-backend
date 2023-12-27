from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Info
from .serializer import TinyInfoSerializer
import environ
import datetime as dt

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


def diff_day(s1):
    d1 = dt.datetime.strptime(s1 + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    date_diff = dt.datetime.now() - d1
    return date_diff.days


class PostInfos(APIView):

    def post(self, request, secret):
        try:
            if secret == env("POST_SECRET_KEY"):
                serializer = TinyInfoSerializer(data=request.data)
                if serializer.is_valid():
                    info = serializer.save()
                    serializer = TinyInfoSerializer(info)
                    return Response(serializer.data)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GetAllInfos(APIView):
    def get(self, request):
        try:
            all_infos = Info.objects.all()
            serializer = TinyInfoSerializer(
                all_infos,
                many=True,
            )
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
# class GetTodayInfos(APIView):
#     def get(self, request):
#         try:
#             # all_infos = Info.objects.all()
#             # serializer = TinyInfoSerializer(
#             #     all_infos,
#             #     many=True,
#             # )
#             return Response(serializer.data)
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
class DeleteInfos(APIView):
    def get(self,request):
        try:
            infos = Info.objects.all()
            for info in infos:
                if diff_day(info.date) > 14:
                    info.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)