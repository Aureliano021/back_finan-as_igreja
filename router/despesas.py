from http import HTTPStatus

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from connection import engine
from models.models import Despesas, User
from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas.schemas import DespesaCreate
from security.auth import get_current_user
from service.db_utils import post_db, update_db, delete_db

router = APIRouter(prefix="/despesas", tags=["despesas"], dependencies=[Depends(get_current_user)])

@router.get("")
async def get_despesas():
    with Session(engine) as session:
        result_despesas = session.execute(select(Despesas)).scalars().all()
    return result_despesas

@router.post("")
async def post_despesas(despesa_create: DespesaCreate):
    despesa = Despesas(nome=despesa_create.nome, valor=despesa_create.valor, data=despesa_create.data)
    post_db(despesa, "Despesa create error")
    return  JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "Despesa created"})

@router.patch("/{despesas_id}")
async def put_despesas(despesas_id: int, despesa_update: DespesaCreate):
    update_db(despesas_id, despesa_update, Despesas, "Despesa update error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Despesa updated"})

@router.delete("/{despesas_id}")
async def delete_despesas(despesas_id: int):
    delete_db(despesas_id, Despesas, "Despesa delete error")
    return JSONResponse(status_code=204, content={"message": "Despesa deleted"})