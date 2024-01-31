from django.urls import path
from . import views

urlpatterns = [
    path("getAll", views.GetAllInfos.as_view()),
    path("getToday", views.GetTodayInfos.as_view()),
    path("deleteInfos", views.DeleteInfos.as_view()),
    path("make-error", views.make_error),
    path("<str:secret>", views.PostInfos.as_view()),
]
