"""anwesend Feld zur User Tabelle hinzufügen

Revision ID: 40ac4d8befdf
Revises: 693ae54e21fa
Create Date: 2022-11-18 10:16:02.949910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "40ac4d8befdf"
down_revision = "693ae54e21fa"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("anwesend", sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("anwesend")

    # ### end Alembic commands ###
