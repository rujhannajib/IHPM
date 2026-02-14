import os
import mysql.connector
from mysql.connector import Error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ihpmdb.db")

# print(BASE_DIR, DB_PATH)
def get_connection(): 
    return mysql.connector.connect( 
        host="localhost", 
        user="ihpmadmin", 
        password="ihpmadmin", 
        database="ihpmdb" ) 