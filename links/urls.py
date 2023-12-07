from django.urls import path
from . import views

urlpatterns = [
    path("all/<str:getsecret>", views.AllLinks.as_view()),
    path("addlink", views.AddLink.as_view()),
    path("me", views.MyLink.as_view()),
]
