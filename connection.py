import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()

def get_engine():
    user = os.getenv("DB_USER")
    password = quote_plus(os.getenv("DB_PASSWORD"))
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine_db = create_engine(url)
    return engine_db

engine = get_engine()

def get_db():
    with Session(engine) as session:
        yield session