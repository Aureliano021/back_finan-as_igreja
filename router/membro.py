from fastapi import APIRouter
from fastapi.params import Depends

from connection import get_engine
from models.models import Membro, User
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer

from schemas.schemas import MembroCreate
from security.auth import get_current_user

engine = get_engine()
router = APIRouter(prefix="/membro")


@router.get("")
async def get_membros(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        result_membros = session.execute(select(Membro)).scalars().all()
    return result_membros

@router.post("")
def post_membros(membro: MembroCreate, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        session.add(membro)


