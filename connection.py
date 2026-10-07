import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()

def get_engine():

    target = os.getenv("DB_TARGET", "local").lower()

    if target == "celular" or target == "server":
        user = os.getenv("DB_SERVER_USER")
        password = quote_plus(os.getenv("DB_SERVER_PASSWORD", ""))
        host = os.getenv("DB_SERVER_HOST")
        port = os.getenv("DB_SERVER_PORT")
        database = os.getenv("DB_SERVER_NAME")
    else:
        user = os.getenv("DB_LOCAL_USER")
        password = quote_plus(os.getenv("DB_LOCAL_PASSWORD", ""))
        host = os.getenv("DB_LOCAL_HOST")
        port = os.getenv("DB_LOCAL_PORT")
        database = os.getenv("DB_LOCAL_NAME")

    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine_db = create_engine(url)
    return engine_db

engine = get_engine()

def get_db():
    with Session(engine) as session:
        yield session