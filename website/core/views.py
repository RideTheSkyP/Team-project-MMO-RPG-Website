from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from .forms import SignUpForm
from .databaseInteraction import DatabaseInteraction
import json


def startPage(request):
    return render(request, "base.html")


@login_required()
def home(request):
    # todo add global statistics overview (must be like a dashboard)
    rows = DatabaseInteraction().homePage(request.user.id)
    return render(request, "home.html", {"stats": rows})


@user_passes_test(lambda u: u.is_anonymous, login_url="home")
def loginToAcc(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required()
def logoutFromAcc(request):
    logout(request)
    return redirect("start")


@user_passes_test(lambda u: u.is_anonymous, login_url="home")
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


class NameForm(forms.Form):
    your_name = forms.CharField(label="Player stats", max_length=100)


def statistics(request):

    rows = DatabaseInteraction().statistics()

    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            return redirect(str("/statistics/" + form.cleaned_data['your_name'] + "/"))
    else:
        form = NameForm()

    return render(request, "statistics.html", {"stats": rows, "form": form})


def player_stats(request, playerNick):
    rows = DatabaseInteraction().getPlayerStats(playerNick)
    favoriteVehicle = DatabaseInteraction().getFavoriteVehicle(rows[0])
    return render(request, "player_stats.html", {"nick": playerNick, "stats": rows, "fav_vehicle": favoriteVehicle})


def test(request):
    return JsonResponse({'works?': 'yes'})


def top_players_all(request):
    json_output = json.dumps(DatabaseInteraction().topPlayersOverall())
    return HttpResponse(json_output)
    # return JsonResponse({"works?": "error"})


@login_required()
def changePassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return render(request, "home.html", {"additionalInfo": "Password changed successfully"})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "changePassword.html", {"form": form})
