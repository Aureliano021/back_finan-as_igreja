from security.auth import get_current_user
from models.models import User
from schemas.schemas import CargoUpdate, CargoCreate
from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from connection import get_db
from models.models import Cargos
from sqlalchemy.orm import Session


from service.db_utils import post_db, delete_db, DBUpdater

router = APIRouter(prefix="/cargos")

@router.get("")
def get_cargos(session: Annotated[Session, Depends(get_db)]):
    cargos = session.query(Cargos).all()
    return cargos

@router.post("")
async def post_cargo(
        session: Annotated[Session, Depends(get_db)],
        cargo: CargoCreate,
        user: Annotated[User, Depends(get_current_user)]
):
    cargos = Cargos(
        membro_id=cargo.membro_id,
        preletor=cargo.preletor,
        dirigente=cargo.dirigente,
        cantor=cargo.cantor,
        musico=cargo.musico,
        tesoureiro=cargo.tesoureiro
    )
    post_db(session, cargos, "Cargo create error")
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "Cargo created successfully"})

@router.patch("/{cargo_id}")
async def patch_cargo(
        session: Annotated[Session, Depends(get_db)],
        cargo: CargoUpdate,
        cargo_id: int,
        user: Annotated[User, Depends(get_current_user)]
):
    DBUpdater(session, cargo_id, cargo, Cargos,"Cargo update error").update()
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Cargo updated successfully"})

@router.delete("/{cargo_id}")
async def delete_cargo(
        session: Annotated[Session, Depends(get_db)],
        cargo_id: int,
        user: Annotated[User, Depends(get_current_user)]
):
    delete_db(session, cargo_id, Cargos, "Cargo delete error")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Cargo deleted successfully"})