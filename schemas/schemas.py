from datetime import date

from pydantic import BaseModel

class DespesaCreate(BaseModel):
    nome: str
    data: date
    valor: int

class DizimoCreate(BaseModel):
    membro_id: int
    valor: float
    data: date

class MembroCreate(BaseModel):
    nome: str
    data_nascimento: date
    membro: bool
    batizado: bool
    uniao_estavel: bool

class OfertasCreate(BaseModel):
    valor: float
    data: date


