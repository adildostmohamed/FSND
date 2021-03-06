"""empty message

Revision ID: a530c182a7c2
Revises: c6d18bd4a56f
Create Date: 2020-05-02 14:35:15.568421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a530c182a7c2'
down_revision = 'c6d18bd4a56f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('start_time', sa.DateTime(), nullable=False),
                    sa.Column('venue_id', sa.Integer(), nullable=False),
                    sa.Column('artist_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
                    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.alter_column('Artist', 'seeking_venue',
                    existing_type=sa.BOOLEAN(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'seeking_venue',
                    existing_type=sa.BOOLEAN(),
                    nullable=True)
    op.drop_table('Show')
    # ### end Alembic commands ###
