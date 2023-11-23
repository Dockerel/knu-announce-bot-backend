from django.contrib import admin
from .models import Info


@admin.register(Info)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "info_type",
        "title",
        "href",
        "date",
        "owner",
    )
