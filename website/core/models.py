from django.db import models
from django.contrib.auth.models import User


# class stat_player_game(models.Model):
# 	teams = (("red", "red"), ("blue", "blue"),)
# 	vehicles = (("walk", "walk"), ("bike", "bike"), ("car", "car"),)
# 	player = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE)
# 	game_id = models.IntegerField()
# 	player_points = models.IntegerField()
# 	team = models.CharField(choices=teams, max_length=5)
# 	vehicle = models.CharField(choices=vehicles, max_length=5)
# 	distance = models.IntegerField(default=None)
# 	team_points = models.IntegerField(default=None)
# 	map = models.CharField(max_length=30, default=None)
# 	won = models.IntegerField(default=None)
#
#
# class top_players(models.Model):
# 	player = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE)
# 	games_won = models.IntegerField(default=None)
# 	percent_won = models.IntegerField(default=None)
# 	avg_points = models.FloatField(default=None)
# 	contribution = models.FloatField(default=None)
#
#
# class stat_map_game(models.Model):
# 	teams = (("red", "red"), ("blue", "blue"),)
# 	game_id = models.IntegerField()
# 	map = models.CharField(max_length=30)
# 	start_time = models.DateTimeField()
# 	end_time = models.DateTimeField()
# 	team_red_points = models.IntegerField()
# 	team_blue_points = models.IntegerField()
# 	team_won = models.CharField(choices=teams, default=None, max_length=5)
#
# 	won = models.IntegerField(default=None)
#
#
# class top_map(models.Model):
# 	map = models.CharField(max_length=30)
# 	no_of_games = models.IntegerField()
# 	avg_time = models.DateTimeField()
# 	max_points_team = models.IntegerField()
# 	avg_points = models.FloatField()
