"""security groups autoscaling storage

Revision ID: ef53ad265c44
Revises: 
Create Date: 2026-05-02 16:42:02.737459

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite
revision = 'ef53ad265c44'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('virtual_machines', schema=None) as batch_op:
        batch_op.drop_column('security_groups')

def downgrade():
    with op.batch_alter_table('virtual_machines', schema=None) as batch_op:
        batch_op.add_column(sa.Column('security_groups', sqlite.JSON(), nullable=True))
