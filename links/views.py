from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .models import Link
from .serializer import LinkSerializer
import environ, requests

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


class AllLinks(APIView):
    def get(self, request, getsecret):
        if env("GET_SECRET_KEY") != getsecret:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            all_links = Link.objects.all()
            serializer = LinkSerializer(
                all_links,
                many=True,
                context={"request": request},
            )
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AddLink(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user):
        try:
            return Link.objects.get(owner=user)
        except ObjectDoesNotExist:
            return Link.objects.create(link="", owner=user)

    def put(self, request):
        targetlink = request.data.get("link")
        print(f"targetlink : {targetlink}")
        if targetlink == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        response = requests.post(
            request.data.get("link"), {"content": "test content..."}
        )
        if response.status_code != 204:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        link = self.get_object(request.user)
        serializer = LinkSerializer(
            link,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            link = serializer.save()
            serializer = LinkSerializer(link)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class MyLink(APIView):
    def get_object(self, user):
        try:
            return Link.objects.get(owner=user)
        except ObjectDoesNotExist:
            raise NotFound

    def get(self, request):
        link = self.get_object(request.user)
        serializer = LinkSerializer(link)
        return Response(serializer.data)

    def put(self, request):
        link = self.get_object(request.user)
        serializer = LinkSerializer(
            link,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_link = serializer.save()
            serializer = LinkSerializer(updated_link)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
