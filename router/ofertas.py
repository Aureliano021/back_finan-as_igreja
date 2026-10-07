from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.models import User, Ofertas

from connection import get_db
from schemas.schemas import OfertasCreate
from security.auth import get_current_user, is_admin
from service.db_utils import post_db, update_db, delete_db


router = APIRouter(prefix="/ofertas", tags=["ofertas"])

@router.get("")
async def get_ofertas(
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    result_oferta = session.execute(select(Ofertas)).scalars().all()
    return result_oferta

@router.post("")
async def post_ofertas(
        oferta_create: OfertasCreate,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    is_admin(user)
    oferta = Ofertas(valor=oferta_create.valor, data=oferta_create.data)
    post_db(session, oferta, "Oferta create error")
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "Oferta created"})

@router.patch("/{oferta_id}")
async def put_ofertas(
        oferta_id: int,
        oferta_update: OfertasCreate,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    is_admin(user)
    update_db(session, oferta_id, oferta_update, Ofertas, "Oferta update error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Oferta updated"})

@router.delete("/{oferta_id}")
async def delete_ofertas(
        oferta_id: int,
        session: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)]
):
    is_admin(user)
    delete_db(session, oferta_id, Ofertas, "Oferta delete error")
    return JSONResponse(status_code=204, content={"message": "Oferta deleted"})