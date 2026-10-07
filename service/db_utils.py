from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from connection import get_engine

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

class DBUpdater:

    def __init__(self, db: Session, object_id: int, object_data, table_db, error_message):
        self.db = db
        object_db = db.get(table_db, object_id)
        if object_db is None:
            raise HTTPException(status_code=404, detail="Not found")
        self.object_db = object_db
        self.object_data = object_data
        self.error_message = error_message

    def many(self, Model, item_name):

        new_data = getattr(self.object_data, item_name, None)
        if new_data is None:
            return self

        data = getattr(self.object_db, item_name)
        data.clear()

        for item in new_data:
            item_data = item.model_dump(exclude_unset=True)
            new_item = Model(**item_data)
            data.append(new_item)
        return self

    def update(self):
        new_data = self.object_data.model_dump(exclude_unset=True)
        for key, value in new_data.items():
            if isinstance(value, list):
                continue
            setattr(self.object_db, key, value)

        try:
            self.db.commit()
            self.db.refresh(self.object_db)
            return self.object_db
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=409, detail=self.error_message)


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