from sqlalchemy import Column, UUID, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base
import uuid


class ExtraContribution(Base):
    __tablename__ = 'extra_contribution'

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('client.id'), nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey('plan.id'), nullable=False)
    contribution_value = Column(DECIMAL(10, 2), nullable=False)

    _clients = relationship('Client', back_populates='_extra_contributions')
    _plans = relationship('Plan', back_populates='_extra_contributions')

