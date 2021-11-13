"""First migration

Revision ID: b610a95d6cd9
Revises: 
Create Date: 2021-11-13 16:17:19.485894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b610a95d6cd9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('license_number', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spaces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('zone_id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('start_x', sa.Integer(), nullable=False),
    sa.Column('start_y', sa.Integer(), nullable=False),
    sa.Column('end_x', sa.Integer(), nullable=False),
    sa.Column('end_y', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('token_expire_time', sa.Float(), nullable=True),
    sa.Column('cookie', sa.String(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('spaces')
    op.drop_table('cars')
    # ### end Alembic commands ###
