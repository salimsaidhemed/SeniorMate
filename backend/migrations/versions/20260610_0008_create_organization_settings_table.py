"""create organization settings table

Revision ID: 20260610_0008
Revises: 20260610_0007
Create Date: 2026-06-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "20260610_0008"
down_revision = "20260610_0007"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "organization_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_name", sa.String(length=255), nullable=True),
        sa.Column("app_display_name", sa.String(length=120), nullable=True),
        sa.Column("logo_object_key", sa.String(length=1024), nullable=True),
        sa.Column("logo_file_name", sa.String(length=255), nullable=True),
        sa.Column("logo_mime_type", sa.String(length=100), nullable=True),
        sa.Column("logo_file_size", sa.BigInteger(), nullable=True),
        sa.Column("primary_color", sa.String(length=7), nullable=True),
        sa.Column("secondary_color", sa.String(length=7), nullable=True),
        sa.Column("accent_color", sa.String(length=7), nullable=True),
        sa.Column("sidebar_color", sa.String(length=7), nullable=True),
        sa.Column("login_banner_text", sa.Text(), nullable=True),
        sa.Column("footer_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("logo_object_key"),
    )


def downgrade():
    op.drop_table("organization_settings")
