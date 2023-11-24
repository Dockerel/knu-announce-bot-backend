from django.urls import path
from . import views

urlpatterns = [
    path("all/<str:secret>", views.Infos.as_view()),
]
