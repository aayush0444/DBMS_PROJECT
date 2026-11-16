
import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root@0999",
            database="academic_review_system",
            port=3306
        )

        return connection

    except mysql.connector.Error as error:
        print("Database connection failed:", error)
        return None
