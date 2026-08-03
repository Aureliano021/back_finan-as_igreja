from fastapi import HTTPException
from psycopg2._psycopg import IntegrityError
from sqlalchemy.orm import Session

from connection import get_engine

engine = get_engine()

def post_db(data):
    with Session(engine) as session:
        session.add(data)
        session.commit()