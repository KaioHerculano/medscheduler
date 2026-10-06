from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rotation_groups",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("spacing_hours", sa.Integer(), nullable=False, server_default="2"),
    )

    op.create_table(
        "medications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "ANALGESIC",
                "ANTIBIOTIC",
                "GASTRIC_PROTECTION",
                "MUSCLE_RELAXANT",
                "ANTIEMETIC",
                name="medicationcategory",
            ),
            nullable=False,
        ),
        sa.Column("min_interval_hours", sa.Integer(), nullable=False, server_default="6"),
        sa.Column("is_as_needed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "rotation_group_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("rotation_groups.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    op.create_table(
        "doses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "medication_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("medications.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("taken_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "status",
            sa.Enum("PENDING", "TAKEN", "SNOOZED", "SKIPPED", name="dosestatus"),
            nullable=False,
            server_default="PENDING",
        ),
        sa.Column("telegram_message_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("doses")
    op.drop_table("medications")
    op.drop_table("rotation_groups")
    op.execute("DROP TYPE IF EXISTS dosestatus;")
    op.execute("DROP TYPE IF EXISTS medicationcategory;")
