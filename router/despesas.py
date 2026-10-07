from security.auth import is_admin
from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from connection import get_db
from models.models import Despesas, User
from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas.schemas import DespesaCreate, DespesaUpdate
from security.auth import get_current_user
from service.db_utils import post_db, update_db, delete_db

router = APIRouter(prefix="/despesas", tags=["despesas"])

@router.get("")
async def get_despesas(
        session: Annotated[Session, Depends(get_db)],
):

    result_despesas = session.execute(select(Despesas)).scalars().all()
    return result_despesas

@router.post("")
async def post_despesas(
        despesa_create: DespesaCreate,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    is_admin(user)
    despesa = Despesas(nome=despesa_create.nome, valor=despesa_create.valor, data=despesa_create.data)
    post_db(session, despesa, "Despesa create error")
    return  JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "Despesa created"})

@router.patch("/{despesas_id}")
async def put_despesas(
        despesas_id: int,
        despesa_update: DespesaUpdate,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    is_admin(user)
    update_db(session, despesas_id, despesa_update, Despesas, "Despesa update error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Despesa updated"})

@router.delete("/{despesas_id}")
async def delete_despesas(
        despesas_id: int,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    is_admin(user)
    delete_db(session, despesas_id, Despesas, "Despesa delete error")
    return JSONResponse(status_code=204, content={"message": "Despesa deleted"})