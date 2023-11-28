from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ParseError
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import TinyUserSerializer, TinyUserSerializer
import environ, json

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


class SignUp(APIView):
    def post(self, request):
        password = request.data.get("password")
        password_check = request.data.get("password_check")
        username = request.data.get("username")
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
