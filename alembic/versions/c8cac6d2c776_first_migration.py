"""first_migration

Revision ID: c8cac6d2c776
Revises: 
Create Date: 2024-11-02 01:52:08.521438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = 'c8cac6d2c776'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('client',
        sa.Column('id', sa.UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False),
        sa.Column('cpf', sa.String(length=11), nullable=False),
        sa.Column('name', sa.String(length=320), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('gender', sa.Enum('Masculino', 'Feminino', 'Outro ', name='gender_enum'), nullable=False),
        sa.Column('monthly_income', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.PrimaryKeyConstraint('id')
                    )

    op.create_table(
        'products',
        sa.Column('id', sa.UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(320), nullable=False),
        sa.Column('susep', sa.String(20), nullable=False),
        sa.Column('expiration_of_sale', sa.DateTime(320), nullable=False),
        sa.Column('value_minimum_aporte_initial', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('value_minimum_aporte_extra', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('entry_age', sa.Integer, nullable=False),
        sa.Column('age_of_exit', sa.Integer, nullable=False),
        sa.Column('lack_initial_of_rescue', sa.Integer, nullable=False),
        sa.Column('lack_entre_resgates', sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('plan',
        sa.Column('id', sa.UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False),
        sa.Column('client_id', sa.UUID, sa.ForeignKey('client.id'), nullable=False),
        sa.Column('contribution', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('product_id', sa.UUID, sa.ForeignKey('products.id'), nullable=False),
        sa.Column('date_of_contract', sa.DateTime(timezone=True), nullable=False),
        sa.Column('age_of_retirement', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('extra_contribution',
        sa.Column('id', sa.UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False),
        sa.Column('contribution_value', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('plan_id', sa.UUID, sa.ForeignKey('plan.id'), nullable=False),
        sa.Column('client_id', sa.UUID, sa.ForeignKey('client.id'), nullable=False),
        sa.PrimaryKeyConstraint('id')
                    )

    op.create_table(
        'rescue',
        sa.Column('id', sa.UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4),
        sa.Column('rescue_value', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('plan_id', sa.UUID, sa.ForeignKey('plan.id'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    pass
