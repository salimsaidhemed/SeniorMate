"""create aide notes table

Revision ID: 20260531_0003
Revises: 20260531_0002
Create Date: 2026-05-31 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "20260531_0003"
down_revision = "20260531_0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "aide_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("visit_id", sa.Integer(), nullable=False),
        sa.Column("personal_care", sa.JSON(), nullable=True),
        sa.Column("nutrition", sa.JSON(), nullable=True),
        sa.Column("mental_status", sa.JSON(), nullable=True),
        sa.Column("elimination", sa.JSON(), nullable=True),
        sa.Column("activity", sa.JSON(), nullable=True),
        sa.Column("assistive_devices", sa.JSON(), nullable=True),
        sa.Column("housekeeping", sa.JSON(), nullable=True),
        sa.Column("additional_notes", sa.Text(), nullable=True),
        sa.Column("aide_name", sa.String(length=200), nullable=False),
        sa.Column("signature_data", sa.Text(), nullable=True),
        sa.Column("signature_date", sa.Date(), nullable=True),
        sa.Column("time_in", sa.Time(), nullable=True),
        sa.Column("time_out", sa.Time(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["visit_id"], ["visits.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("visit_id", name="uq_aide_notes_visit_id"),
    )
    op.create_index("ix_aide_notes_patient_id", "aide_notes", ["patient_id"])
    op.create_index("ix_aide_notes_visit_id", "aide_notes", ["visit_id"], unique=True)


def downgrade():
    op.drop_index("ix_aide_notes_visit_id", table_name="aide_notes")
    op.drop_index("ix_aide_notes_patient_id", table_name="aide_notes")
    op.drop_table("aide_notes")
