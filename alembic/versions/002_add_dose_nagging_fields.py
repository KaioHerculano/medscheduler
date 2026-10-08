from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = '002_add_dose_nagging_fields'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'doses',
        sa.Column('last_notified_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        'doses',
        sa.Column(
            'reminder_count',
            sa.Integer(),
            nullable=False,
            server_default='0',
        ),
    )


def downgrade() -> None:
    op.drop_column('doses', 'reminder_count')
    op.drop_column('doses', 'last_notified_at')
