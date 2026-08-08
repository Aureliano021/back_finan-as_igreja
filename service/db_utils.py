from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import Update

from connection import get_engine

engine = get_engine()

def post_db(object_data, message_error):
    with Session(engine) as session:
        try:
            session.add(object_data)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=409,
                                detail=message_error)
        session.refresh(object_data)

def put_db(object_id: int, object_data, table_db, message_error):
    with Session(engine) as session:
        try:
            object_db = session.get(table_db, object_id)
            if object_db is None:
                raise HTTPException(status_code=404, detail="Not found")

            new_data = object_data.model_dump(exclude_unset=True)
            for key, value in new_data.items():
                setattr(object_db, key, value)

            session.commit()
            session.refresh(object_db)
            return object_db
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=409,
                                detail=message_error)

def delete_db(object_id: int, table_db, message_error):
    with Session(engine) as session:
        try:
            object_db = session.get(table_db, object_id)
            if object_db is None:
                raise HTTPException(status_code=404, detail="Not found")
            session.delete(object_db)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=409,
                                detail=message_error)