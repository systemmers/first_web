"""empty message

Revision ID: 618ce142246a
Revises: 
Create Date: 2024-07-14 17:46:19.009111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '618ce142246a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question')
    # ### end Alembic commands ###
