from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Link


class TinyLinkSerializer(ModelSerializer):
    class Meta:
        model = Link
        fields = (
            "info_type",
            "title",
            "link",
            "date",
        )
