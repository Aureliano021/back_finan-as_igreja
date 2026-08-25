import json
from http import HTTPStatus

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from connection import engine
from models.models import Membro, User
from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas.schemas import MembroCreate, MembroUpdate
from security.auth import get_current_user
from service.db_utils import post_db, update_db, delete_db

router = APIRouter(prefix="/membro", dependencies=[Depends(get_current_user())])

@router.get("")
async def get_membros():
    with Session(engine) as session:
        result_membros = session.execute(select(Membro)).scalars().all()
    return result_membros

@router.post("")
async def post_membros(membro_create: MembroCreate):
    membro = Membro(nome=membro_create.nome,
                    data_nascimento=membro_create.data_nascimento,
                    membro=membro_create.membro,
                    batizado=membro_create.batizado,
                    uniao_estavel=membro_create.uniao_estavel
                    )

    post_db(membro, "Membro create error")
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "Membro created"})

@router.patch("/{membro_id:int}")
async def put_membros(membro_id: int, membro_update: MembroUpdate):
    update_db(membro_id, membro_update, Membro, "Membro update error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Membro updated"})


@router.delete("/{membro_id:int}")
async def delete_membros(membro_id: int):
    delete_db(membro_id, Membro, "Membro delete error")
    return JSONResponse(status_code=204, content={"message": "Membro deleted"})