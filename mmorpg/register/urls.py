from django.contrib import admin
from django.urls import path, include
from .views import say

urlpatterns = [
	path("", say, name="hello")
]