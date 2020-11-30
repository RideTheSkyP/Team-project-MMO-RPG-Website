import mysql.connector

config = {
  "user": "sql2379354",
  "password": "vE2*dN8!",
  "host": "sql2.freemysqlhosting.net",
  "database": "sql2379354",
  "raise_on_warnings": True
}


class Database:
    def __init__(self):
        self.db = mysql.connector.connect(**config)

    def addUser(self, login, password):
        cursor = self.db.cursor()
        query = "insert into user_details(login, password, email) values (%s, %s, %s)"
        values = (login, password, "email")
        cursor.execute(query, values)
        self.db.commit()
        print(f"User {login} added")
        self.db.close()
