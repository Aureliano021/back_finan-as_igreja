from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from typing import Annotated
from connection import get_db
from schemas.auth_schemas import Login, Register

from fastapi import APIRouter, HTTPException

from security.auth import tokenizer, auth_user, register_user


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(
        user_login: Login,
        session: Annotated[Session, Depends(get_db)]
):
    user = auth_user(session, user_login.email, user_login.senha)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    token = tokenizer(user.nome, user.email)
    return JSONResponse(status_code=200, content={
        "message": "login successful",
        "access_token": token,
        "token_type": "bearer"
    })

@router.post("/register")
# pyrefly: ignore [bad-function-definition]
async def register(
        user_register: Register,
        session: Annotated[Session, Depends(get_db)]
):
    register_user(user_register, session)
    return JSONResponse(status_code=201, content={
        "message": "register successful, wait for authorization."
    })