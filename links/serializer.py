from rest_framework.serializers import ModelSerializer
from .models import Link
from users.models import User


class TinyLinkUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class TinyLinkSerializer(ModelSerializer):
    class Meta:
        model = Link
        fields = ("link",)


class LinkSerializer(ModelSerializer):
    owner = TinyLinkUsernameSerializer(read_only=True)

    class Meta:
        model = Link
        fields = (
            "link",
            "owner",
        )
