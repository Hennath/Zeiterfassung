"""Buchungen Tabelle

Revision ID: 8b044a091fc2
Revises: 15c6c6a16385
Create Date: 2022-11-14 15:31:05.621283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8b044a091fc2"
down_revision = "15c6c6a16385"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "buchungen",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("buchungen", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_buchungen_timestamp"), ["timestamp"], unique=False
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("buchungen", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_buchungen_timestamp"))

    op.drop_table("buchungen")
    # ### end Alembic commands ###
