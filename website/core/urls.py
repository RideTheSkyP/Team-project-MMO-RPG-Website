from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.startPage, name="start"),
    path("home/", views.home, name="home"),
    path("login/", views.loginToAcc, name="login"),
    path("logout/", views.logoutFromAcc, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("statistics/", views.statistics, name="statistics"),
    path("statistics/<str:player_nick>", views.player_stats, name="player_stats"),
]
