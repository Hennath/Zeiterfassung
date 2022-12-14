"""changed name fields in user model

Revision ID: 06018e21f5cf
Revises: c98b896c67f0
Create Date: 2022-11-15 14:39:32.151835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "06018e21f5cf"
down_revision = "c98b896c67f0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("vorname", sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column("nachname", sa.String(length=64), nullable=True))
        batch_op.drop_index("ix_user_username")
        batch_op.create_index(
            batch_op.f("ix_user_nachname"), ["nachname"], unique=False
        )
        batch_op.create_index(batch_op.f("ix_user_vorname"), ["vorname"], unique=False)
        batch_op.drop_column("username")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("username", sa.VARCHAR(length=64), nullable=True))
        batch_op.drop_index(batch_op.f("ix_user_vorname"))
        batch_op.drop_index(batch_op.f("ix_user_nachname"))
        batch_op.create_index("ix_user_username", ["username"], unique=False)
        batch_op.drop_column("nachname")
        batch_op.drop_column("vorname")

    # ### end Alembic commands ###
