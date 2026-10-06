"""database finanças igreja

Revision ID: fc730d7e0d55
Revises: 
Create Date: 2026-07-24 16:47:59.391772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc730d7e0d55'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'membros',
        sa.Column('id', sa.Integer(),primary_key=True),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('data_nascimento', sa.Date(), nullable=False ),
        sa.Column('cpf', sa.String(11), unique=True),
        sa.Column('cep', sa.String(8)),
        sa.Column('endereco', sa.String(255)),
        sa.Column('email', sa.String(150)),
        sa.Column('celular', sa.String(15))
    )

    op.create_table(
        'dizimos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('membro_id', sa.Integer(), sa.ForeignKey('membros.id'), nullable=False),
        sa.Column('valor', sa.Numeric(10,2), nullable=False),
        sa.Column('data', sa.Date(), nullable=False)
    )

    op.create_table(
        'ofertas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('valor', sa.Numeric(10,2), nullable=False),
        sa.Column('data', sa.Date(), nullable=False),
    )

    op.create_table(
        'despesas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(255), nullable=False ),
        sa.Column('valor', sa.Numeric(10,2), nullable=False),
        sa.Column('data', sa.Date(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('dizimos')
    op.drop_table('membros')
    op.drop_table('ofertas')
    op.drop_table('despesas')

