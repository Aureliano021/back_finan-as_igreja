import fastapi
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from connection import get_engine
from models.models import *
from router.membro import router as membro_router
from router.login import router as login_router
from security.auth import get_current_user

engine = get_engine()
app = fastapi.FastAPI()

app.include_router(membro_router)
app.include_router(login_router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/membros")
def get_membros(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        result_membros = session.execute(select(Membro)).scalars().all()
    return result_membros

@app.get("/dizimos")
def get_dizimos(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        result_dizimos = session.execute(select(Dizimos)).scalars().all()
    return result_dizimos

@app.get("/despesas")
def get_despesas(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        result_despesas = session.execute(select(Despesas)).scalars().all()
    return result_despesas

@app.get("/ofertas")
def get_membros(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        result_ofertas = session.execute(select(Ofertas)).scalars().all()
    return result_ofertas