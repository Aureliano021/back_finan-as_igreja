from starlette.responses import JSONResponse

from connection import get_engine
from schemas.auth_schemas import Login, Register

from fastapi import APIRouter, HTTPException

from security.auth import pwt_context, tokenizer, auth_user, register_user

engine = get_engine()

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(user_login: Login):
    user = auth_user(user_login.email, user_login.senha)
    if user is False:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    token = tokenizer(user.nome, user.email)
    return JSONResponse(status_code=200, content={
        "message": "login successful",
        "access_token": token,
        "token_type": "bearer"
    })

@router.post("/register")
async def register(user_register: Register):
    register_user(user_register)
    return JSONResponse(status_code=201, content={
        "message": "register successful, wait for authorization."
    })