from django.urls import path
from .views import say, signup

urlpatterns = [
	# path("", say, name="hello"),
	path("", signup, name="signup"),
]
