from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from django.contrib.auth import authenticate, login, logout
from .models import User
from links.models import Link
from infos.models import Info
from .serializers import TinyUserSerializer
from links.serializer import LinkSerializer
from infos.serializer import TinyInfoSerializer
import environ, json
import datetime as dt
from discord_webhook import DiscordWebhook

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


class SignUp(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        password_check = request.data.get("password_check")
        if User.objects.filter(username=username).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if password != password_check or not password or not password_check:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = TinyUserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(password)
            new_user.save()
            serializer = TinyUserSerializer(new_user)

            user = authenticate(
                request,
                username=username,
                password=password,
            )
            login(request, user)

            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = TinyUserSerializer(user)
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        if not User.objects.filter(username=username).exists():
            return Response(
                {"error": "No username"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response(
                {"ok": "Welcome"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"ok": "Bye"},
            status=status.HTTP_200_OK,
        )


class DeleteErrorUsers(APIView):
    def post(self, request, postsecret):
        if env("POST_SECRET_KEY") != postsecret:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        error_links = json.loads(request.data)
        for link in error_links:
            user = User.objects.get(username=link.get("owner")["username"])
            user.delete()
        return Response(status=status.HTTP_200_OK)


class SendToday(APIView):
    def __init__(self):
        d = dt.datetime.now()
        self.today = f"{d.year}-{str(d.month).zfill(2)}-{str(d.day).zfill(2)}"

    def get_link(self, user):
        try:
            link = Link.objects.get(owner=user)
            return link
        except:
            raise NotFound

    def get_infos(self):
        try:
            infos = Info.objects.filter(date=self.today)
            return infos
        except:
            raise NotFound

    def get(self, request):
        try:
            link = self.get_link(request.user)
            infos = self.get_infos()

            linkdata = LinkSerializer(link)
            mylink = linkdata.data.get("link")

            infodata = TinyInfoSerializer(infos, many=True).data

            if len(infodata) > 0:
                temp_msg = ""
                temp_msg += "=" * 10
                for d in infodata:
                    info_type = d["info_type"]
                    title = d["title"]
                    href = d["href"]
                    temp_msg += f"\n{self.today} | {info_type}\n{title}\n{href}\n"
                temp_msg += "=" * 10
            else:
                temp_msg = "=" * 10
                temp_msg += "\nNo announcement today...\n"
                temp_msg += "=" * 10

            webhook = DiscordWebhook(url=mylink, content=temp_msg)
            webhook.execute()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SendAll(APIView):
    def get_link(self, user):
        try:
            link = Link.objects.get(owner=user)
            return link
        except:
            raise NotFound

    def get_infos(self):
        try:
            infos = Info.objects.all()
            return infos
        except:
            raise NotFound

    def get(self, request):
        try:
            link = self.get_link(request.user)
            infos = self.get_infos()

            linkdata = LinkSerializer(link)
            mylink = linkdata.data.get("link")

            infodata = TinyInfoSerializer(infos, many=True).data

            temp_msg = "=" * 10
            pre_date = ""
            for d in infodata:
                if pre_date != d["date"]:
                    if len(temp_msg) > 10:
                        temp_msg += "=" * 10
                        # 전송
                        webhook = DiscordWebhook(url=mylink, content=temp_msg)
                        webhook.execute()
                    pre_date = d["date"]
                    temp_msg = "=" * 10

                info_type = d["info_type"]
                title = d["title"]
                href = d["href"]
                temp_msg += f"\n{pre_date} | {info_type}\n{title}\n{href}\n"
            if len(temp_msg) > 10:
                temp_msg += "=" * 10
                # 전송
                webhook = DiscordWebhook(url=mylink, content=temp_msg)
                webhook.execute()

            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
