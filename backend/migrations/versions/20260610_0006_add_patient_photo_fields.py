"""add patient photo fields

Revision ID: 20260610_0006
Revises: 20260609_0005
Create Date: 2026-06-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "20260610_0006"
down_revision = "20260609_0005"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("patients") as batch_op:
        batch_op.add_column(sa.Column("photo_object_key", sa.String(1024)))
        batch_op.add_column(sa.Column("photo_file_name", sa.String(255)))
        batch_op.add_column(sa.Column("photo_mime_type", sa.String(100)))
        batch_op.add_column(sa.Column("photo_file_size", sa.BigInteger()))
        batch_op.add_column(sa.Column("photo_uploaded_at", sa.DateTime(timezone=True)))
        batch_op.add_column(
            sa.Column(
                "photo_verified",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )
        batch_op.create_unique_constraint(
            "uq_patients_photo_object_key",
            ["photo_object_key"],
        )


def downgrade():
    with op.batch_alter_table("patients") as batch_op:
        batch_op.drop_constraint(
            "uq_patients_photo_object_key",
            type_="unique",
        )
        batch_op.drop_column("photo_verified")
        batch_op.drop_column("photo_uploaded_at")
        batch_op.drop_column("photo_file_size")
        batch_op.drop_column("photo_mime_type")
        batch_op.drop_column("photo_file_name")
        batch_op.drop_column("photo_object_key")
