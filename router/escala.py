from schemas.schemas import EscalaUpdate, EscalaItemUpdate, EscalaCreate
from security.auth import is_admin
from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from connection import get_db
from models.models import Despesas, User, Escala, EscalaItem
from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas.schemas import DespesaCreate, DespesaUpdate
from security.auth import get_current_user
from service.db_utils import post_db, update_db, delete_db, DBUpdater
from service.escala.escala import montar_escalas

router = APIRouter(prefix="/escala")

@router.get("/suggestion")
async def get_suggestion_escala(
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    escala = montar_escalas(session)

    return escala

@router.get("/item")
async def get_escala_item(
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    escala = session.execute(select(EscalaItem)).scalars().all()
    return escala

@router.get("/item/{escala_item_id:int}")
async def get_escala_item_by_id(
        escala_item_id: int,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    escala = session.execute(select(EscalaItem).where(EscalaItem.id == escala_item_id)).scalar()
    if escala is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "Item não encontrado"})
    return escala

from sqlalchemy.orm import selectinload

@router.get("")
async def get_escalas(
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    stmt = select(Escala).options(selectinload(Escala.itens))
    return session.execute(stmt).scalars().all()

@router.get("/{escala_id}")
async def get_escala_by_id(
        escala_id: int,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    escala = session.execute(select(Escala).where(Escala.id == escala_id)).scalar()
    if escala is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "Escala não encontrada"})

    return escala

@router.post("")
async def post_escala(
        escala: EscalaCreate,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    nova_escala = Escala(
        data=escala.data,
        descricao=escala.descricao,
        itens=[
            EscalaItem(
                membro_id = item.membro_id,
                funcao = item.funcao
            )
            for item in escala.itens
        ]

    )
    session.add(nova_escala)
    session.commit()
    session.refresh(nova_escala)

    return JSONResponse(status_code=HTTPStatus.CREATED, content={"id": nova_escala.id})

@router.put("/{escala_id}")
async def put_escala(
        escala_id: int,
        escala: EscalaUpdate,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    (DBUpdater(session, escala_id, escala, Escala, "Escala update error")
     .many(EscalaItem, "itens")
     .update())

    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Escala atualizada com sucesso"})

@router.delete("/{escala_id}")
async def delete_escala(
        escala_id: int,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    delete_db(session, escala_id, Escala, "Escala delete error")

    return JSONResponse(status_code=204, content={"message": "Escala deletada com sucesso"})

