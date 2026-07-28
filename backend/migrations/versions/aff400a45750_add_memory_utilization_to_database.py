
from alembic import op
import sqlalchemy as sa

revision = 'aff400a45750'
down_revision = 'ef53ad265c44'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('databases', schema=None) as batch_op:
        batch_op.add_column(sa.Column('memory_utilization', sa.Float(), nullable=True))

def downgrade():
    with op.batch_alter_table('databases', schema=None) as batch_op:
        batch_op.drop_column('memory_utilization')
