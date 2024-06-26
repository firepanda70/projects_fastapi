"""final

Revision ID: 16f83778af11
Revises: 
Create Date: 2024-05-12 03:22:12.253702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16f83778af11'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('user_pkey')),
    sa.UniqueConstraint('username', name=op.f('user_username_key'))
    )
    op.create_table('project',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('stage', sa.Enum('INIT', 'PLAN', 'EXEC', 'CNTRL', 'CLOSE', name='projectstage'), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name=op.f('project_owner_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('project_pkey'))
    )
    op.create_table('group',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('frozen_group', sa.Boolean(), nullable=False),
    sa.Column('proj_edit', sa.Boolean(), nullable=False),
    sa.Column('proj_delete', sa.Boolean(), nullable=False),
    sa.Column('group_read', sa.Boolean(), nullable=False),
    sa.Column('group_create', sa.Boolean(), nullable=False),
    sa.Column('group_edit', sa.Boolean(), nullable=False),
    sa.Column('group_delete', sa.Boolean(), nullable=False),
    sa.Column('group_grant', sa.Boolean(), nullable=False),
    sa.Column('group_revoke', sa.Boolean(), nullable=False),
    sa.Column('request_read', sa.Boolean(), nullable=False),
    sa.Column('request_edit', sa.Boolean(), nullable=False),
    sa.Column('partis_delete', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], name=op.f('group_project_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('group_pkey')),
    sa.UniqueConstraint('name', 'project_id', name=op.f('group_name_key'))
    )
    op.create_table('partisipant',
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], name=op.f('partisipant_project_id_fkey')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('partisipant_user_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('partisipant_pkey'))
    )
    op.create_table('partisipation_request',
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('user_from_id', sa.Integer(), nullable=False),
    sa.Column('processed_by_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('NEW', 'ACCEPTED', 'DENIED', name='requeststatus'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['processed_by_id'], ['user.id'], name=op.f('partisipation_request_processed_by_id_fkey')),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], name=op.f('partisipation_request_project_id_fkey')),
    sa.ForeignKeyConstraint(['user_from_id'], ['user.id'], name=op.f('partisipation_request_user_from_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('partisipation_request_pkey'))
    )
    op.create_table('group_to_partisipant',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('partisipant_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], name=op.f('group_to_partisipant_group_id_fkey')),
    sa.ForeignKeyConstraint(['partisipant_id'], ['partisipant.id'], name=op.f('group_to_partisipant_partisipant_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('group_to_partisipant_pkey'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group_to_partisipant')
    op.drop_table('partisipation_request')
    op.drop_table('partisipant')
    op.drop_table('group')
    op.drop_table('project')
    op.drop_table('user')
    # ### end Alembic commands ###
