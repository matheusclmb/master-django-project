from django.urls import path, include

from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    path("signup/", view=views.signup, name="signup"),
    path("weather/", view=views.weather, name="weather"),
    path("movie/", view=views.movie, name="movie"),

]
