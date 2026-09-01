from fastapi import HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from connection import get_engine, get_db

engine = get_engine()

def post_db(db: Session, object_data, message_error):
    try:
        db.add(object_data)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,
                            detail=message_error)
    db.refresh(object_data)

def update_db(db: Session, object_id: int, object_data, table_db, message_error):
    try:
        object_db = db.get(table_db, object_id)
        if object_db is None:
            raise HTTPException(status_code=404, detail="Not found")

        new_data = object_data.model_dump(exclude_unset=True)
        for key, value in new_data.items():
            setattr(object_db, key, value)

        db.commit()
        db.refresh(object_db)
        return object_db
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,
                            detail=message_error)

def delete_db(db: Session, object_id: int, table_db, message_error):
    try:
        object_db = db.get(table_db, object_id)
        if object_db is None:
            raise HTTPException(status_code=404, detail="Not found")
        db.delete(object_db)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,
                            detail=message_error)