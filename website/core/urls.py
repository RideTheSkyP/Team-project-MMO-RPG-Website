from django.urls import path
from . import views

urlpatterns = [
    path("", views.startPage, name="start"),
    path("home/", views.home, name="home"),
    path("login/", views.loginToAcc, name="login"),
    path("signup/", views.signup, name="signup"),
]
