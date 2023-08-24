"""Init

Revision ID: da26fc59c713
Revises: 
Create Date: 2023-08-06 11:33:21.737285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da26fc59c713'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('surname', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('phone', sa.String(length=150), nullable=False),
    sa.Column('bd', sa.DATE(), nullable=False),
    sa.Column('city', sa.String(length=150), nullable=False),
    sa.Column('notes', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contacts_email'), 'contacts', ['email'], unique=True)
    op.create_index(op.f('ix_contacts_name'), 'contacts', ['name'], unique=False)
    op.create_index(op.f('ix_contacts_phone'), 'contacts', ['phone'], unique=False)
    op.create_index(op.f('ix_contacts_surname'), 'contacts', ['surname'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_contacts_surname'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_phone'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_name'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_email'), table_name='contacts')
    op.drop_table('contacts')
    # ### end Alembic commands ###
