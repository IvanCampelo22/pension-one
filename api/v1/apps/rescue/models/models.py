from sqlalchemy import Column, UUID, DECIMAL, ForeignKey
from database.session import Base
from sqlalchemy.orm import relationship
import uuid


class Rescue(Base):
    __tablename__ = 'rescue'

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    plan_id = Column(UUID(as_uuid=True), ForeignKey('plan.id'), nullable=False)
    rescue_value = Column(DECIMAL(10, 2), nullable=False)

    _plans = relationship('Plan', back_populates='_rescues')
