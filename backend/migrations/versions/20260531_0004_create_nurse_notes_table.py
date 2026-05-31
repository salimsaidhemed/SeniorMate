"""create nurse notes table

Revision ID: 20260531_0004
Revises: 20260531_0003
Create Date: 2026-05-31 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "20260531_0004"
down_revision = "20260531_0003"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "nurse_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("visit_id", sa.Integer(), nullable=False),
        sa.Column("diagnosis", sa.Text(), nullable=True),
        sa.Column("living_arrangements", sa.JSON(), nullable=True),
        sa.Column("visit_type", sa.JSON(), nullable=True),
        sa.Column("vital_signs", sa.JSON(), nullable=True),
        sa.Column("diet", sa.JSON(), nullable=True),
        sa.Column("pain_assessment", sa.JSON(), nullable=True),
        sa.Column("sensory", sa.JSON(), nullable=True),
        sa.Column("neuro", sa.JSON(), nullable=True),
        sa.Column("respiratory", sa.JSON(), nullable=True),
        sa.Column("cardiac", sa.JSON(), nullable=True),
        sa.Column("peripheral_circulation", sa.JSON(), nullable=True),
        sa.Column("genitourinary", sa.JSON(), nullable=True),
        sa.Column("gastrointestinal", sa.JSON(), nullable=True),
        sa.Column("endocrine", sa.JSON(), nullable=True),
        sa.Column("skin_integrity", sa.JSON(), nullable=True),
        sa.Column("wound_evaluation", sa.JSON(), nullable=True),
        sa.Column("mental_status", sa.JSON(), nullable=True),
        sa.Column("functional_status", sa.JSON(), nullable=True),
        sa.Column("homebound_status", sa.JSON(), nullable=True),
        sa.Column("skilled_nursing", sa.Text(), nullable=True),
        sa.Column("response_to_intervention", sa.Text(), nullable=True),
        sa.Column("patient_caregiver_understanding", sa.JSON(), nullable=True),
        sa.Column("md_contact", sa.JSON(), nullable=True),
        sa.Column("discharge_planning", sa.Text(), nullable=True),
        sa.Column("patient_feedback", sa.Text(), nullable=True),
        sa.Column("narrative", sa.Text(), nullable=True),
        sa.Column("signature_data", sa.Text(), nullable=True),
        sa.Column("signature_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["visit_id"], ["visits.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("visit_id", name="uq_nurse_notes_visit_id"),
    )
    op.create_index("ix_nurse_notes_patient_id", "nurse_notes", ["patient_id"])
    op.create_index("ix_nurse_notes_visit_id", "nurse_notes", ["visit_id"], unique=True)


def downgrade():
    op.drop_index("ix_nurse_notes_visit_id", table_name="nurse_notes")
    op.drop_index("ix_nurse_notes_patient_id", table_name="nurse_notes")
    op.drop_table("nurse_notes")
