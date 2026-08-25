from datetime import datetime
from datetime import date

from decimal import Decimal
from sqlalchemy import String, Date, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression
from sqlalchemy import func

from .base import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(8), nullable=False, server_default="pendente")
    date_created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

class Despesas(Base):
    __tablename__ = "despesas"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)

class Dizimos(Base):
    __tablename__ = "dizimos"
    id: Mapped[int] = mapped_column(primary_key=True)
    membro_id: Mapped[int] = mapped_column(ForeignKey("membros.id"),nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)

class Membro(Base):
    __tablename__ = "membros"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255),nullable=False)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=True)
    membro: Mapped[bool] = mapped_column(server_default=expression.false())
    batizado: Mapped[bool] = mapped_column(server_default=expression.false())
    uniao_estavel: Mapped[bool] = mapped_column(server_default=expression.false())

class Ofertas(Base):
    __tablename__ = "ofertas"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    data: Mapped[date] = mapped_column( Date ,nullable=False)

class Logs(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(100), nullable=True)
    details: Mapped[str] = mapped_column(String(255), nullable=True)
