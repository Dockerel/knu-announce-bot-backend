from django.db import models
from common.models import CommonModel


class Info(CommonModel):

    """Info Model Definition"""

    class announceKindChoices(models.TextChoices):
        GENERAL = ("general", "General")
        BACHELOR = ("bachelor", "Bachelor")
        SCHOLARSHIP = ("scholarship", "Scholarship")
        SIMCOM = ("simcom", "Simcom")
        GLSOB = ("glsob", "Glsob")
        INCOM = ("incom", "Incom")
        GRADUATE = ("graduate", "Graduate")
        CONTRACT = ("contract", "Contract")

    info_type = models.CharField(
        max_length=100,
        choices=announceKindChoices.choices,
    )
    title = models.CharField(max_length=100)
    href = models.CharField(max_length=100)
    date = models.CharField(max_length=12)

    def __str__(self) -> str:
        return f"{self.info_type} / {self.title[:8]}..."
