"""Add twitter to donation

Revision ID: 05fe10dccba2
Revises: b425315cc865
Create Date: 2019-05-14 21:28:40.055964

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "05fe10dccba2"
down_revision = "b425315cc865"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("donation", sa.Column("twitter", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("donation", "twitter")
    # ### end Alembic commands ###
