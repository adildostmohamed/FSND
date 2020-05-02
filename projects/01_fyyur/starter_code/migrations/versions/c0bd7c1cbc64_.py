"""empty message

Revision ID: c0bd7c1cbc64
Revises: a530c182a7c2
Create Date: 2020-05-02 18:43:54.412539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0bd7c1cbc64'
down_revision = 'a530c182a7c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('Artist', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('Show', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('Show', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('Venue', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('Venue', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'updated_at')
    op.drop_column('Venue', 'created_at')
    op.drop_column('Show', 'updated_at')
    op.drop_column('Show', 'created_at')
    op.drop_column('Artist', 'updated_at')
    op.drop_column('Artist', 'created_at')
    # ### end Alembic commands ###
