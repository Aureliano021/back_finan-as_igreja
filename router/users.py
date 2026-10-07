from schemas.schemas import UserUpdate
from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.models import User

from connection import get_db
from security.auth import get_current_user, is_admin
from service.db_utils import post_db, update_db, delete_db


router = APIRouter(prefix="/users")

@router.get("/")
def get_users(
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    users = session.execute(select(User)).scalars().all()
    return users

@router.patch("/{user_id}")
def patch_user(
        user_id: int,
        user_update: UserUpdate,
        session: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
):
    is_admin(current_user)
    update_db(session, user_id,user_update, User, "User update error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "User updated successfully"})

@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        session: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
):
    is_admin(current_user)
    delete_db(session, user_id, User, "User delete error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "User deleted successfully"})