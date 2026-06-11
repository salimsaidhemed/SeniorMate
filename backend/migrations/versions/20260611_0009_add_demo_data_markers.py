"""add demo data markers

Revision ID: 20260611_0009
Revises: 20260610_0008
Create Date: 2026-06-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "20260611_0009"
down_revision = "20260610_0008"
branch_labels = None
depends_on = None


TABLES = (
    "patients",
    "visits",
    "aide_notes",
    "nurse_notes",
    "patient_assessments",
    "medical_records",
)


def upgrade():
    for table in TABLES:
        op.add_column(
            table,
            sa.Column(
                "is_demo_data",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        )
        op.create_index(
            op.f(f"ix_{table}_is_demo_data"),
            table,
            ["is_demo_data"],
            unique=False,
        )


def downgrade():
    for table in reversed(TABLES):
        op.drop_index(op.f(f"ix_{table}_is_demo_data"), table_name=table)
        op.drop_column(table, "is_demo_data")
