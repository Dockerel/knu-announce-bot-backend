from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Info


class TinyInfoSerializer(ModelSerializer):
    class Meta:
        model = Info
        fields = (
            "info_type",
            "title",
            "link",
            "date",
        )
