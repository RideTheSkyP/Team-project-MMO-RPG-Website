from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from .forms import SignUpForm, NameForm
from .databaseInteraction import DatabaseInteraction
import json
from django.db import connection
from datetime import datetime, date, time


def startPage(request):
    return render(request, "base.html")


@login_required()
def home(request):
    # todo add global statistics overview (must be like a dashboard)
    # rows = DatabaseInteraction().statsLastGames(request.user.id)
    # mystats = DatabaseInteraction().getPlayerStats(request.user.username)
    return render(request, "home.html", {})


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


"""
statystyki
"""
def statistics(request):
    rows = DatabaseInteraction().statsTopPlayers()

    maps = DatabaseInteraction().statsTopMaps()

    last_games = ""

    if request.user.id is not None:
        last_games = DatabaseInteraction().statsLastGames(request.user.id)


    for i, row in enumerate(maps):
        print(row)
        temp_row = (row[0], row[1], datetime.combine(date.min, row[2]) - datetime.min, row[3], row[4])
        if i == 0:
            new_maps = temp_row
        else:
            new_maps = (new_maps,) + (temp_row,)


    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():

            return redirect(str("/statistics/" + form.cleaned_data['playerNickname'] + "/"))
            # rows = DatabaseInteraction().getPlayerStats(form.cleaned_data['playerNickname'])

            # return render(request, "statistics.html", {"stats": rows})
    else:
        form = NameForm()

    return render(request, "statistics.html", {"stats": rows, "form": form, "maps": new_maps, "last_games": last_games})


def player_stats(request, player_nick):

    rows = DatabaseInteraction().getPlayerStats(player_nick)

    fav_vehicle = ""
    fav_map = ""

    try:
        fav_vehicle = DatabaseInteraction().getFavoriteVehicle(rows[0])
        fav_map = DatabaseInteraction().getFavoriteMap(rows[0])
    except Exception:
        pass

    return render(request, "player_stats.html", {"nick": player_nick, "stats": rows, "fav_vehicle": fav_vehicle, "fav_map": fav_map})


def map_stats(request, the_map):

    rows = DatabaseInteraction().getMapStats(the_map)
        
    avg_time = datetime.combine(date.min, rows[2]) - datetime.min
    
    tot_dist = DatabaseInteraction().getMapTotalDistance(the_map)

    km_pkt = float(tot_dist[1]) / rows[4]

    return render(request, "map_stats.html", {"map": the_map, "stats": rows, "avg_time": avg_time, \
        "tot_dist": tot_dist, "km_pkt": km_pkt})

def test(request):
    return JsonResponse({'works?': 'yes'})

"""
koniec statystyk
"""


""" 
API 
"""
def top_players_all(request):

    with connection.cursor() as cursor:
        try:
            cursor.execute("""SELECT player_id, Nick, games_won, percent_won, \
                avg_points, contribution FROM top_players""")

            r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
            # print(r)
            json_output = json.dumps(r)
            return HttpResponse(json_output)

        except Exception as e:
            print(e)

    return JsonResponse({"works?": "error"})

def top_maps(request):
    with connection.cursor() as cursor:
        try:
            # TODO ogarnąć avg_time
            cursor.execute("""SELECT map, no_of_games, max_points_team, \
            	avg_points FROM top_map order by no_of_games desc LIMIT 100""")

            r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]

            json_output = json.dumps(r)
            return HttpResponse(json_output)

        except Exception as e:
            print(e)

    return JsonResponse({"works?": "error"})

"""
koniec API
"""


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
