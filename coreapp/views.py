from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import redirect, render

import requests
from coreapp.forms import SignUpForm
from django.contrib.auth import authenticate, login

from coreapp.forms import CityForm
from .models import City

# Create your views here.


def home(request):
    return render(request, "coreapp/pages/home.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get("password1")

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect("/")

    else:
        form = SignUpForm()
    return render(request, "coreapp/pages/signup.html", {"form": form})


def weather(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ddda7ff1dea2fcd997bac92e74f9185f"

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            "city": city.name,
            "temperature": r["main"]["temp"],
            "description": r["weather"][0]["description"],
            "icon": r["weather"][0]["icon"],
        }

        weather_data.append(city_weather)

    context = {"weather_data": weather_data, "form": form}

    return render(request, "coreapp/pages/weather.html", context)
