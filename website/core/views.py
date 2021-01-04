from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from core.databaseConnection import Database
from django.db import connection
from django import forms


def startPage(request):
    return render(request, "base.html")


@login_required()
def home(request):
    return render(request, "home.html")


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


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

def statistics(request):

    with connection.cursor() as cursor:
        cursor.execute("""SELECT player_id, Nick, games_won, percent_won, \
        avg_points, contribution FROM top_players order by games_won desc LIMIT 10""")
        rows = cursor.fetchall()


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
        # cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        try:
            cursor.execute("""SELECT player_id, Nick, games_won, percent_won, \
                avg_points, contribution FROM top_players WHERE Nick = %s""", [player_nick])
            rows = cursor.fetchone()
            # print(rows[0])

        except Exception:
            print("ups")
            return redirect("home") 

        fav_vehicle = ""

        try:
            cursor.execute("""SELECT vehicle, count(*) AS magnitude FROM stat_player_game \
                WHERE player_id like %s \
                GROUP BY vehicle \
                ORDER BY magnitude DESC LIMIT 1""", [rows[0]])
            fav_vehicle = cursor.fetchone()

        except Exception:
            print("ups")

    print(fav_vehicle)

    return render(request, "player_stats.html", {"nick": player_nick, "stats": rows, "fav_vehicle": fav_vehicle})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            # db = Database()
            # db.addUser(username, password)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})
