from django.urls import path
from . import views

urlpatterns = [
    path("infos/<str:secret>", views.Infos.as_view()),
]
