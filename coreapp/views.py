from multiprocessing import context
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.urls import reverse, reverse_lazy
from unicodedata import name
from requests.models import HTTPError
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

import requests
from coreapp.forms import SignUpForm, ToDoForm, ContactForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail


from coreapp.forms import CityForm
from .models import City,  ToDoItem

import tmdbsimple as tmdb
import random
import json
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



        if not City.objects.filter(name=form.data["name"]).exists():
            form.save()



    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    try:
        for city in cities:
            r = requests.get(url.format(city)).json()

            if r["cod"] != "404":
                city_weather = {
                    "city": city.name,
                    "temperature": r["main"]["temp"],
                    "description": r["weather"][0]["description"],
                    "icon": r["weather"][0]["icon"],
                }

                weather_data.append(city_weather)

            elif r["cod"] == "404":
                messages.error(request, "City not found. Try again.")
                city.delete()
            
    except KeyError:
        return HttpResponse("Error: City not found. Please delete from database. @ http://localhost:8000/admin/")

    context = {"weather_data": weather_data, "form": form}

    return render(request, "coreapp/pages/weather.html", context)


def movie(request):

    tmdb.API_KEY = "b02201f7ff269ad539f084c9223efc3e"

    movie = tmdb.Movies()
    random_page = movie.popular(page=random.randint(1, 100))
    movie_id = random_page["results"][random.randint(1, 19)]["id"]
    random_movie = tmdb.Movies(movie_id)
    movie_info = random_movie.info()
    movie_credits = random_movie.credits()

    try:
        context = {"title": random_movie.title,
                   "release": random_movie.release_date,
                   "author": random_movie.crew[0]["name"],
                   "poster": random_movie.poster_path,
                   "overview": random_movie.overview, 
                   "id": movie_id,}
    except IndexError:
        context = {"title": random_movie.title,
                   "release": random_movie.release_date,
                   "author": "No Director found",
                   "poster": random_movie.poster_path,
                   "overview": random_movie.overview, 
                   "id": movie_id,}
    except HTTPError:
        raise Http404("Movie not found")

    return render(request, "coreapp/pages/moviegen.html", context)


def todo(request):

    item_list = ToDoItem.objects.order_by("-created_date")
    if request.method == "POST":
        form = ToDoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo')
    form = ToDoForm()

    page = {
        "forms": form,
        "list": item_list,
        "title": "TODO LIST",
    }
    return render(request, 'coreapp/pages/todoapp.html', page)


def del_item(request, item_id):
    item = ToDoItem.objects.get(id=item_id)
    item.delete()
    messages.info(request, "Item removed.")
    return redirect('todo')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            email_subject  = f"New contact {form.cleaned_data['name']} < {form.cleaned_data['email']} > : {form.cleaned_data['subject']}"
            email_message  = f"{form.cleaned_data['message']}"
            send_mail(email_subject, email_message, settings.CONTACT_EMAIL, [settings.ADMIN_EMAIL])
            context = {"sucess": "Thank you for your message. Will get back to you soon."}
            return render(request, "coreapp/pages/contact.html", context)
    form = ContactForm()
    context = {"form": form}
    return render(request, "coreapp/pages/contact.html", context)