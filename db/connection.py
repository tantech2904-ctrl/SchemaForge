import mysql.connector as c
from mysql.connector import Error

def get_connection():
    try:
        connection = c.connect(
            host="localhost",
            user="root",
            password="root",
            database="dbmanager"
        )
        return connection
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None
