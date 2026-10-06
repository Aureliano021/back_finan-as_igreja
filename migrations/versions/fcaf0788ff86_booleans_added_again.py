"""booleans added, again

Revision ID: fcaf0788ff86
Revises: fc730d7e0d55
Create Date: 2026-07-24 20:26:55.975996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression

# revision identifiers, used by Alembic.
revision: str = 'fcaf0788ff86'
down_revision: Union[str, Sequence[str], None] = 'fc730d7e0d55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'membros',
        sa.Column('membro', sa.Boolean(), server_default=expression.false(), nullable=False),
    )
    op.add_column(
        'membros',
        sa.Column('batizado', sa.Boolean(), server_default=expression.false(), nullable=False),
    )
    op.add_column(
        'membros',
        sa.Column('uniao_estavel', sa.Boolean(), server_default=expression.false(), nullable=False),
    )


def downgrade() -> None:

    op.drop_column('membros', 'membro')
    op.drop_column('membros', 'batizado')
    op.drop_column('membros', 'uniao_estavel')