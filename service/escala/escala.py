from typing import List, Sequence

import random

from models.models import Cargos
from sqlalchemy import select, text

from models.models import Membro
from sqlalchemy.orm import Session

def montar_escalas(session: Session):
    escala = {
        "preletor": None,
        "dirigente": None,
        "cantor": None,
        "musico": None,
    }

    membros_escalados = set()
    for cargo, nome in escala.items():
        membros_list: Sequence[Membro] = buscar_membro(session, cargo)
        if not membros_list:
            continue
        membros_disponiveis = [m for m in membros_list if m.id not in membros_escalados]

        membros = membros_disponiveis if membros_disponiveis else membros_list
        membro = random.choice(membros)
        membros_escalados.add(membro.id)
        escala[cargo] = membro.nome
    return escala

def buscar_membro(session: Session, cargo: str):

    coluna_cargo = getattr(Cargos, cargo)
    stmt = (
        select(Membro)
        .join(Cargos ,Cargos.membro_id == Membro.id)
        .where(coluna_cargo == True)
    )

    return session.scalars(stmt).all()
