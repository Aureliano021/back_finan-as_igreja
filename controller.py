import fastapi

from starlette.middleware.cors import CORSMiddleware
from connection import get_engine

from router.membro import router as membro_router
from router.login import router as login_router
from router.ofertas import router as ofertas_router
from router.dizimos import router as dizimos_router
from router.despesas import router as despesas_router

engine = get_engine()
app = fastapi.FastAPI()

app.include_router(membro_router)
app.include_router(login_router)
app.include_router(ofertas_router)
app.include_router(dizimos_router)
app.include_router(despesas_router)


origins = [
    "http://192.168.1.40",
    "http://192.168.1.83",
    "http://localhost",          # Acesso local
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.get('/health')
def health():
    return {'status': 'ok'}