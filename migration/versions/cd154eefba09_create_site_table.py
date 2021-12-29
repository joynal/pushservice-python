"""create site table

Revision ID: cd154eefba09
Revises: 
Create Date: 2021-12-28 07:17:26.291344

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'cd154eefba09'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "site",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
            unique=True,
        ),
        sa.Column("public_key", sa.TEXT, nullable=False),
        sa.Column("private_key", sa.TEXT, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=func.now()),
        sa.Index("site_id_index", "id")
    )


def downgrade():
    op.drop_table("site")
