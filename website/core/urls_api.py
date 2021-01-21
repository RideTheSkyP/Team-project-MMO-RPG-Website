from django.urls import path, include
from . import views

# warte zanotowania - wszystkie są tu z przedrostkiem api, więc test to api/test
urlpatterns = [
    path("test", views.test, name="test"),
    path("top_players_all", views.top_players_all, name="top_players_all"),
    path("top_maps", views.top_maps, name="top_maps")
]
