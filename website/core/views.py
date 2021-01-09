from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection
from django import forms
from .forms import SignUpForm
import json


def startPage(request):
    return render(request, "base.html")


@login_required()
def home(request):

    # statystyki
    # strona: róbcie z tym co chcecie, wrzuciłem to na zasadzie że ładnie może wyglądać
    with connection.cursor() as cursor:

        rows = ""
        try:
            cursor.execute("""SELECT player_id, player_points, team, team_points, map, won, id FROM stat_player_game \
                WHERE id = %s order by id desc limit 10""", [request.user.id])
            rows = cursor.fetchall()

        except Exception as e:
            print(e)

    passed_data = {
        "stats": rows
    }

    return render(request, "home.html", passed_data)


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
    your_name = forms.CharField(label='Statystiki gracza:', max_length=100)


def statistics(request):
    with connection.cursor() as cursor:
        rows = ""
        try:
            cursor.execute("""SELECT player_id, Nick, games_won, percent_won, \
                avg_points, contribution FROM top_players order by games_won desc LIMIT 10""")
            rows = cursor.fetchall()
        except Exception as e:
            print(e)

    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return redirect(str("/statistics/" + form.cleaned_data['your_name'] + "/"))
    else:
        form = NameForm()

    print(rows)
    return render(request, "statistics.html", {"stats": rows, "form": form})


def player_stats(request, player_nick):
    with connection.cursor() as cursor:
        rows = ""
        try:
            cursor.execute("""SELECT player_id, Nick, games_won, percent_won, \
                avg_points, contribution FROM top_players WHERE Nick = %s""", [player_nick])
            rows = cursor.fetchone()
            # print(rows[0])

        except Exception as e:
            print(e)
            # return redirect("statistics")

        fav_vehicle = ""
        try:
            cursor.execute("""SELECT vehicle, count(*) AS magnitude FROM stat_player_game \
                WHERE player_id like %s \
                GROUP BY vehicle \
                ORDER BY magnitude DESC LIMIT 1""", [rows[0]])
            fav_vehicle = cursor.fetchone()

        except Exception as e:
            print(e)

    print(fav_vehicle)

    return render(request, "player_stats.html", {"nick": player_nick, "stats": rows, "fav_vehicle": fav_vehicle})


def test(request):
    return JsonResponse({'works?': 'yes'})


def top_players_all(request):
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT player_id, Nick, games_won, percent_won, avg_points, contribution FROM top_players")
            r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            # print(r)
            json_output = json.dumps(r)

            return HttpResponse(json_output)

        except Exception as e:
            print(e)

    return JsonResponse({"works?": "error"})
