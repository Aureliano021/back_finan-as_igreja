import decimal
from datetime import date
from typing import Optional

from decimal import Decimal
from pydantic import BaseModel

class DespesaCreate(BaseModel):
    nome: str
    data: date
    valor: Decimal

class DespesaUpdate(BaseModel):
    nome: Optional[str] = None
    data: Optional[date] = None
    valor: Optional[Decimal] = None

class DizimoCreate(BaseModel):
    membro_id: int
    valor: Decimal
    data: date

class DizimoUpdate(BaseModel):
    membro_id: Optional[int] = None
    valor: Optional[Decimal] = None
    data: Optional[date] = None

class MembroCreate(BaseModel):
    nome: str
    data_nascimento: date
    membro: bool
    batizado: bool
    uniao_estavel: bool

class MembroUpdate(BaseModel):
    nome: Optional[str] = None
    data_nascimento: Optional[date] = None
    membro: Optional[bool] = None
    batizado: Optional[bool] = None
    uniao_estavel: Optional[bool] = None

class OfertasCreate(BaseModel):
    valor: Decimal
    data: date

class OfertasUpdate(BaseModel):
    valor: Optional[Decimal] = None
    data: Optional[date] = None


