from django.urls import path
from . import views

urlpatterns = [
    path("", views.SignUp.as_view()),
    path("me", views.Me.as_view()),
    path("signin", views.SignIn.as_view()),
    path("signup", views.SignUp.as_view()),
    path("signout", views.SignOut.as_view()),
    path("sendtoday", views.SendToday.as_view()),
    path("sendall", views.SendAll.as_view()),
    path("delete-errorlink-users/<str:postsecret>", views.DeleteErrorUsers.as_view()),
]
