from django.db import connection


class DatabaseInteraction:
	def __init__(self):
		self.cursor = connection.cursor()

	def homePage(self, userId):
		try:
			self.cursor.execute("""select player_id, player_points, team, team_points, map, won, id 
				from core_stat_player_game where id=%s order by id desc limit 10""", [userId])
			return self.cursor.fetchall()
		except Exception as exc:
			print(f"Home page databaseInt exception: {exc}")

	def statistics(self):
		try:
			self.cursor.execute("""select player_id, username, games_won, percent_won, avg_points, contribution 
				from core_top_players  inner join auth_user on player_id=auth_user.id order by games_won desc LIMIT 10""")
			return self.cursor.fetchall()
		except Exception as exc:
			print(f"Statistics databaseInt exception: {exc}")

	def getPlayerStats(self, playerNick):
		try:
			self.cursor.execute("""select player_id, username, games_won, percent_won, avg_points, contribution 
				from core_top_players inner join auth_user on player_id=auth_user.id where username = %s""", [playerNick])
			row = self.cursor.fetchall()
			return row
		except Exception as exc:
			print(f"Player stats databaseInt exception: {exc}")

	def topPlayersOverall(self):
		try:
			self.cursor.execute("""select player_id, username, games_won, percent_won, avg_points, contribution
				from core_top_players inner join auth_user on player_id=auth_user.id""")
			return [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in self.cursor.fetchall()]
		except Exception as exc:
			print(f"Top players overall databaseInt exception: {exc}")

	def getFavoriteVehicle(self, playerId):
		try:
			self.cursor.execute("""select vehicle, count(*) as magnitude from core_stat_player_game 
				where player_id like %s group by vehicle order by magnitude desc LIMIT 1""", [playerId])
			return self.cursor.fetchone()
		except Exception as exc:
			print(f"Favorite vehicle databaseInt exception: {exc}")
