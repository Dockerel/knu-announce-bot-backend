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


class Infos(APIView):
    def get(self, request, secret):
        if secret == env("GET_SECRET_KEY"):
            all_infos = Info.objects.all()
            serializer = TinyInfoSerializer(
                all_infos,
                many=True,
            )
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, secret):
        if secret == env("POST_SECRET_KEY"):
            # delete
            infos = Info.objects.all()
            for info in infos:
                if diff_day(info.date) > 7:
                    info.delete()

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
