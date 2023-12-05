from django.db import models
from common.models import CommonModel


class Link(CommonModel):

    """Link Model Definition"""

    link = models.CharField(max_length=200,default="")
    owner = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.owner.username
