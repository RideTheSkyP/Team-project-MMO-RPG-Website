import mysql.connector

config = {
    "user": "user",
    "password": "password",
    "host": "34.107.65.104",
    "database": "pz",
    "raise_on_warnings": True,
    'ssl_ca': '/home/push/Downloads/server-ca_4.pem',
    'ssl_key': '/home/push/Downloads/client-key_2.pem',
    'ssl_cert': '/home/push/Downloads/client-cert_2.pem'
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

    def checkConnection(self):
        mycursor = self.db.cursor()
        mycursor.execute("SELECT * FROM user_details")
        myresult = mycursor.fetchall()
        print(myresult)


Database().checkConnection()
