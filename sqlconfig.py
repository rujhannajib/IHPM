import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ihpmdb.db")

# print(BASE_DIR, DB_PATH)
def get_connection(): 
    return mysql.connector.connect( 
        host="localhost", 
        user=os.getenv('DB_USER'), 
        password=os.getenv('DB_PASSWORD'), 
        database=os.getenv('DB_NAME') ) 
    