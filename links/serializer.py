from rest_framework.serializers import ModelSerializer
from .models import Link
from users.serializers import TinyUserSerializer


class TinyLinkSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)

    class Meta:
        model = Link
        fields = (
            "link",
            "owner",
        )
