import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from models.models import User

from connection import get_engine, get_db
from schemas.auth_schemas import Register
from service.db_utils import post_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

load_dotenv()
engine = get_engine()
key = os.getenv("SECRET_KEY")

if key is None:
    raise ValueError("...")

pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def tokenizer(nome: str, email:str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    encode: dict = {"sub": nome, "email": email}
    encode.update({"exp": expire})
    return jwt.encode(encode, key, algorithm="HS256")

def auth_user(session: Session, email: str, senha: str):

    user = session.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.status != "aceito":
        raise HTTPException(status_code=401, detail="User not allowed")
    if user and pwt_context.verify(senha, user.senha):
        return user
    else:
        raise HTTPException(status_code=401, detail="invalid credentials")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), ):
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate user"
        )

    email = payload.get("email")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate user"
        )
    if user.status != "aceito":
        raise HTTPException(
            status_code=401,
            detail="User not allowed"
        )
    return user

def register_user(user: Register, session: Session):
    senha = user.senha
    tamanho = len(senha)

    if tamanho <= 7:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    password = pwt_context.hash(user.senha)
    user_register = User(nome=user.nome, email=user.email, senha=password)
    post_db(session, user_register, "Email already registered")