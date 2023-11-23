from django.contrib import admin
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "info_type",
        "title",
        "link",
        "date",
    )
