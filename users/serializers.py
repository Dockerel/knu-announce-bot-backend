from rest_framework.serializers import ModelSerializer
from .models import User
from links.serializer import TinyLinkSerializer


class TinyUserSerializer(ModelSerializer):
    link = TinyLinkSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "link",
        )


class TinyUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)
