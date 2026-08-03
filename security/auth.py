import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.models import User

from connection import get_engine
from schemas.auth_schemas import Register

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

def auth_user(email: str, senha: str):
    with Session(engine) as session:
        user = session.query(User).filter(User.email == email).first()
        if user.status != "aceito":
            raise HTTPException(status_code=401, detail="User not allowed")
        if user and pwt_context.verify(senha, user.senha):
            return user
        return False

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"])
        nome = payload.get("sub")
        email = payload.get("email")
        with Session(engine) as session:
            user = session.query(User).filter(User.email == email).first()
            if user is None: raise HTTPException(status_code=401, detail="Could not validate user")
            return user
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate user")

def register_user(user: Register):
    password = pwt_context.hash(user.senha)
    user_register = User(nome=user.nome, email=user.email, senha=password)
    with Session(engine) as session:
        try:
            session.add(user_register)
            session.commit()

        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=409, detail="User already registered")
        session.refresh(user_register)
