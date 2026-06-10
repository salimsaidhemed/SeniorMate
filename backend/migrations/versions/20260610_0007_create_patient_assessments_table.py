"""create patient assessments table

Revision ID: 20260610_0007
Revises: 20260610_0006
Create Date: 2026-06-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "20260610_0007"
down_revision = "20260610_0006"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "patient_assessments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("visit_id", sa.Integer(), nullable=True),
        sa.Column("assessment_type", sa.String(length=50), nullable=False),
        sa.Column("assessment_date", sa.Date(), nullable=False),
        sa.Column("performed_by", sa.String(length=200), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("findings", sa.JSON(), nullable=True),
        sa.Column("recommendations", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "assessment_type IN "
            "('fall_risk', 'nutrition', 'mobility', 'cognitive', 'general')",
            name="ck_patient_assessments_type",
        ),
        sa.CheckConstraint(
            "status IN ('draft', 'completed')",
            name="ck_patient_assessments_status",
        ),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patients.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["visit_id"],
            ["visits.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_patient_assessments_patient_id"),
        "patient_assessments",
        ["patient_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_patient_assessments_visit_id"),
        "patient_assessments",
        ["visit_id"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        op.f("ix_patient_assessments_visit_id"),
        table_name="patient_assessments",
    )
    op.drop_index(
        op.f("ix_patient_assessments_patient_id"),
        table_name="patient_assessments",
    )
    op.drop_table("patient_assessments")
