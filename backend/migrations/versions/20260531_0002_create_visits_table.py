"""create visits table

Revision ID: 20260531_0002
Revises: 20260529_0001
Create Date: 2026-05-31 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "20260531_0002"
down_revision = "20260529_0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "visits",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("visit_date", sa.Date(), nullable=False),
        sa.Column("visit_type", sa.String(length=100), nullable=False),
        sa.Column("staff_name", sa.String(length=200), nullable=True),
        sa.Column("staff_role", sa.String(length=50), nullable=True),
        sa.Column("time_in", sa.Time(), nullable=True),
        sa.Column("time_out", sa.Time(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "staff_role IN ('aide', 'nurse')",
            name="ck_visits_staff_role",
        ),
        sa.CheckConstraint(
            "status IN ('scheduled', 'completed', 'cancelled')",
            name="ck_visits_status",
        ),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_visits_patient_id", "visits", ["patient_id"])


def downgrade():
    op.drop_index("ix_visits_patient_id", table_name="visits")
    op.drop_table("visits")
