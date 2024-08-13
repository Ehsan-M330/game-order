"""test alembic configuration by add a number column to games

Revision ID: 11c6e863400d
Revises: 
Create Date: 2024-08-13 16:14:24.659345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11c6e863400d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('games',sa.Column('number',sa.String(),nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('games','number')
    pass
