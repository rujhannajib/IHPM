from sqlconfig import get_connection
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

connection_string = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
engine = create_engine(connection_string)

def export_password():
    # Read directly to DataFrame and export
    uf = pd.read_sql("SELECT * FROM users", engine)
    df = pd.read_sql("SELECT * FROM cred", engine)
    uf.to_csv('users.csv', index=False)
    df.to_csv('passwords.csv', index=False)

    print(f"Exported {len(uf)} rows to users.csv")
    print(f"Exported {len(df)} rows to passwords.csv")