from http import HTTPStatus

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.models import User, Ofertas

from connection import get_engine
from schemas.schemas import OfertasCreate
from security.auth import get_current_user
from service.db_utils import post_db, put_db, delete_db

engine = (get_engine())
router = APIRouter(prefix="/ofertas", tags=["ofertas"])

@router.get("")
async def get_ofertas(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        result_oferta = session.execute(select(Ofertas)).scalars().all()
    return result_oferta

@router.post("")
async def post_ofertas(oferta_create: OfertasCreate, current_user: User = Depends(get_current_user)):
    oferta = Ofertas(valor=oferta_create.valor, data=oferta_create.data)
    post_db(oferta, "Oferta create error")
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "Oferta created"})

@router.put("/{oferta_id}")
async def put_ofertas(oferta_id: int, oferta_update: OfertasCreate, current_user: User = Depends(get_current_user)):
    put_db(oferta_id, oferta_update, Ofertas, "Oferta update error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Oferta updated"})

@router.delete("/{oferta_id}")
async def delete_ofertas(oferta_id: int, current_user: User = Depends(get_current_user)):
    delete_db(oferta_id, Ofertas, "Oferta delete error")
    return JSONResponse(status_code=204, content={"message": "Oferta deleted"})