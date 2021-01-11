from django.db import connection


class DatabaseInteraction:
	def __init__(self):
		self.cursor = connection.cursor()

	def homePage(self, userId):
		try:
			self.cursor.execute("""SELECT player_id, player_points, team, team_points, map, won, id  \
				FROM stat_player_game WHERE id = %s order by id desc limit 10""", [userId])
			return self.cursor.fetchall()
		except Exception as exc:
			print(f"Home page databaseInt exception: {exc}")

	def statistics(self):
		try:
			self.cursor.execute("""SELECT player_id, Nick, games_won, percent_won, avg_points, contribution 
				FROM top_players order by games_won desc LIMIT 10""")
			return self.cursor.fetchall()
		except Exception as exc:
			print(f"Statistics databaseInt exception: {exc}")

	def getPlayerStats(self, playerNick):
		try:
			self.cursor.execute("""SELECT player_id, Nick, games_won, percent_won, avg_points, contribution 
					FROM top_players WHERE Nick = %s""", [playerNick])
			return self.cursor.fetchone()
		except Exception as exc:
			print(f"Player stats databaseInt exception: {exc}")

	def topPlayersOverall(self):
		try:
			self.cursor.execute("""SELECT player_id, Nick, games_won, percent_won, avg_points, contribution
				FROM top_players""")
			return [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in self.cursor.fetchall()]
		except Exception as exc:
			print(f"Top players overall databaseInt exception: {exc}")

	def getFavoriteVehicle(self, playerId):
		try:
			self.cursor.execute("""SELECT vehicle, count(*) AS magnitude FROM stat_player_game \
		        WHERE player_id like %s GROUP BY vehicle ORDER BY magnitude DESC LIMIT 1""", [playerId])
			return self.cursor.fetchone()
		except Exception as exc:
			print(f"Favorite vehicle databaseInt exception: {exc}")
