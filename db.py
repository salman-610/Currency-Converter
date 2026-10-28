
import os

import mysql.connector
from mysql.connector import Error


def connect_database():
    try:
        password = os.getenv("MYSQL_PASSWORD")

        if not password:
            print("MySQL password not found.")
            print("Please set the MYSQL_PASSWORD environment variable.")
            return None

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="currency_converter"
        )

        if connection.is_connected():
            return connection

        connection.close()

    except Error as error:
        print("Database connection failed:", error)

    return None
