from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Link
from .serializer import TinyLinkSerializer


class Links(APIView):
    def get(self, request):
        all_links = Link.objects.all()
        serializer = TinyLinkSerializer(
            all_links,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = TinyLinkSerializer(data=request.data)
        if serializer.is_valid():
            link = serializer.save()
            serializer = TinyLinkSerializer(link)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
