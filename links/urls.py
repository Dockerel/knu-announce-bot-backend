from django.urls import path
from . import views

urlpatterns = [
    path("all", views.AllLinks.as_view()),
    path("addlink", views.AddLink.as_view()),
    path("<str:username>", views.OneLink.as_view()),
]
