from http import HTTPStatus

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.models import User, Dizimos

from connection import get_engine
from schemas.schemas import DizimoCreate, DizimoUpdate
from security.auth import get_current_user
from service.db_utils import post_db, put_db, delete_db

engine = (get_engine())
router = APIRouter(prefix="/dizimos", tags=["dizimos"])

@router.get("")
async def get_dizimos(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        result_dizimo = session.execute(select(Dizimos)).scalars().all()
    return result_dizimo

@router.post("")
async def post_dizimos(dizimo_create: DizimoCreate,current_user: User = Depends(get_current_user)):
    dizimo = Dizimos(membro_id=dizimo_create.membro_id, valor=dizimo_create.valor, data=dizimo_create.data)
    post_db(dizimo, "Dizimo create error")
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "Dizimo created"})

@router.put("/{dizimo_id}")
async def put_dizimos(dizimo_id: int, dizimo_update: DizimoUpdate, current_user: User = Depends(get_current_user)):
    put_db(dizimo_id, dizimo_update, Dizimos, "Dizimo update error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Dizimo updated"})

@router.delete("/{dizimo_id}")
async def delete_dizimo(dizimo_id: int, current_user: User = Depends(get_current_user)):
    delete_db(dizimo_id, Dizimos, "Dizimo delete error")
    return JSONResponse(status_code=204, content={"message": "Dizimo deleted"})
