from security.auth import is_admin
from models.models import User
from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.models import Dizimos

from connection import get_db
from schemas.schemas import DizimoCreate, DizimoUpdate
from security.auth import get_current_user
from service.db_utils import post_db, update_db, delete_db

router = APIRouter(prefix="/dizimos", tags=["dizimos"])

@router.get("")
async def get_dizimos(
        session: Annotated[Session, Depends(get_db)],
):
    result_dizimo = session.execute(select(Dizimos)).scalars().all()
    return result_dizimo

@router.post("")
async def post_dizimos(
        dizimo_create: DizimoCreate,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    is_admin(user)
    dizimo = Dizimos(membro_id=dizimo_create.membro_id, valor=dizimo_create.valor, data=dizimo_create.data)
    post_db(session, dizimo, "Dizimo create error")
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "Dizimo created"})

@router.patch("/{dizimo_id}")
async def put_dizimos(
        dizimo_id: int,
        dizimo_update: DizimoUpdate,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    is_admin(user)
    update_db(session, dizimo_id, dizimo_update, Dizimos, "Dizimo update error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Dizimo updated"})

@router.delete("/{dizimo_id}")
async def delete_dizimo(
        dizimo_id: int,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    is_admin(user)
    delete_db(session, dizimo_id, Dizimos, "Dizimo delete error")
    return HTTPStatus.NO_CONTENT
