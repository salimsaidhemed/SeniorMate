"""create patients table

Revision ID: 20260529_0001
Revises:
Create Date: 2026-05-29 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "20260529_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("gender", sa.String(length=50), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("emergency_contact_name", sa.String(length=200), nullable=True),
        sa.Column("emergency_contact_phone", sa.String(length=50), nullable=True),
        sa.Column("diagnosis_summary", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('active', 'inactive')",
            name="ck_patients_status",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("patients")
