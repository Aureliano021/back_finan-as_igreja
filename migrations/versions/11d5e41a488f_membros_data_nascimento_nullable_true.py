"""membros, data_nascimento: nullable = true

Revision ID: 11d5e41a488f
Revises: fcaf0788ff86
Create Date: 2026-07-24 21:15:44.532816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11d5e41a488f'
down_revision: Union[str, Sequence[str], None] = 'fcaf0788ff86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('membros', 'data_nascimento', nullable=True)


def downgrade() -> None:
    op.alter_column('membros', 'data_nascimento', nullable=False)
