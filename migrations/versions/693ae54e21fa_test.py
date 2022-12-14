"""test

Revision ID: 693ae54e21fa
Revises: 06018e21f5cf
Create Date: 2022-11-15 15:24:37.266459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "693ae54e21fa"
down_revision = "06018e21f5cf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("vorname", sa.String(length=64), nullable=True),
        sa.Column("nachname", sa.String(length=64), nullable=True),
        sa.Column("personalnummer", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_user_nachname"), ["nachname"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_user_personalnummer"), ["personalnummer"], unique=True
        )
        batch_op.create_index(batch_op.f("ix_user_vorname"), ["vorname"], unique=False)

    op.create_table(
        "buchungen",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("kommen", sa.DateTime(), nullable=True),
        sa.Column("gehen", sa.DateTime(), nullable=True),
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
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_user_vorname"))
        batch_op.drop_index(batch_op.f("ix_user_personalnummer"))
        batch_op.drop_index(batch_op.f("ix_user_nachname"))

    op.drop_table("user")
    # ### end Alembic commands ###
