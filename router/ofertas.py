from http import HTTPStatus

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.models import User, Ofertas

from connection import engine
from schemas.schemas import OfertasCreate
from security.auth import get_current_user
from service.db_utils import post_db, update_db, delete_db


router = APIRouter(prefix="/ofertas", tags=["ofertas"], dependencies=[Depends(get_current_user())])

@router.get("")
async def get_ofertas():
    with Session(engine) as session:
        result_oferta = session.execute(select(Ofertas)).scalars().all()
    return result_oferta

@router.post("")
async def post_ofertas(oferta_create: OfertasCreate):
    oferta = Ofertas(valor=oferta_create.valor, data=oferta_create.data)
    post_db(oferta, "Oferta create error")
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "Oferta created"})

@router.patch("/{oferta_id}")
async def put_ofertas(oferta_id: int, oferta_update: OfertasCreate):
    update_db(oferta_id, oferta_update, Ofertas, "Oferta update error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Oferta updated"})

@router.delete("/{oferta_id}")
async def delete_ofertas(oferta_id: int):
    delete_db(oferta_id, Ofertas, "Oferta delete error")
    return JSONResponse(status_code=204, content={"message": "Oferta deleted"})