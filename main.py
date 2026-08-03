import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

print(db_url)