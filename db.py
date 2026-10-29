
import os

import mysql.connector
from mysql.connector import Error


def open_ratebridge_store():
    password_value = os.getenv("MYSQL_PASSWORD")

    if not password_value:
        print("MySQL password is not configured.")
        print("Set the MYSQL_PASSWORD environment variable.")
        return None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password_value,
            database="currency_converter",
        )

        if connection.is_connected():
            return connection

        connection.close()

    except Error as error:
        print("Could not connect to the conversion database:", error)

    return None
