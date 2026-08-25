from http import HTTPStatus

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.models import User, Dizimos

from connection import engine
from schemas.schemas import DizimoCreate, DizimoUpdate
from security.auth import get_current_user
from service.db_utils import post_db, update_db, delete_db

router = APIRouter(prefix="/dizimos", tags=["dizimos"], dependencies=[Depends(get_current_user)])

@router.get("")
async def get_dizimos():
    with Session(engine) as session:
        result_dizimo = session.execute(select(Dizimos)).scalars().all()
    return result_dizimo

@router.post("")
async def post_dizimos(dizimo_create: DizimoCreate):
    dizimo = Dizimos(membro_id=dizimo_create.membro_id, valor=dizimo_create.valor, data=dizimo_create.data)
    post_db(dizimo, "Dizimo create error")
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "Dizimo created"})

@router.patch("/{dizimo_id}")
async def put_dizimos(dizimo_id: int, dizimo_update: DizimoUpdate):
    update_db(dizimo_id, dizimo_update, Dizimos, "Dizimo update error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Dizimo updated"})

@router.delete("/{dizimo_id}")
async def delete_dizimo(dizimo_id: int):
    delete_db(dizimo_id, Dizimos, "Dizimo delete error")
    return HTTPStatus.NO_CONTENT
