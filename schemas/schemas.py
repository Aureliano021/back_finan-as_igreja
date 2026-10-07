
from datetime import date
from typing import Optional, List

from decimal import Decimal
from pydantic import BaseModel

from models.models import FuncaoEscala


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

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None

class EscalaItemCreate(BaseModel):
    membro_id: int
    funcao: FuncaoEscala # aceita: "preletor", "dirigente", "cantor", "músico"

class EscalaCreate(BaseModel):
    data: date
    descricao: str
    itens: List[EscalaItemCreate] = []

class EscalaItemUpdate(BaseModel):
    membro_id: Optional[int] = None
    funcao: Optional[FuncaoEscala] = None

class EscalaUpdate(BaseModel):
    data: Optional[date] = None
    descricao: Optional[str] = None
    itens: Optional[List[EscalaItemUpdate]] = None

class CargoUpdate(BaseModel):
    membro_id: Optional[int] = None
    preletor: Optional[bool] = None
    dirigente: Optional[bool] = None
    cantor: Optional[bool] = None
    musico: Optional[bool] = None
    tesoureiro: Optional[bool] = None

class CargoCreate(BaseModel):
    membro_id: int
    preletor: bool
    dirigente: bool
    cantor: bool
    musico: bool
    tesoureiro: bool
