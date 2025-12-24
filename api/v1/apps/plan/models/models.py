from sqlalchemy import Column, Integer, DateTime, UUID, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base
import uuid


class Plan(Base):
    __tablename__ = 'plan'

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('client.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    contribution = Column(DECIMAL(10, 2), nullable=False)
    date_of_contract = Column(DateTime(timezone=True), nullable=False)
    age_of_retirement = Column(Integer, nullable=False)

    _clients = relationship('Client', back_populates='_plans')
    _products = relationship('Products', back_populates='_plans')
    _extra_contributions = relationship('ExtraContribution', back_populates='_plans')   
    _rescues = relationship('Rescue', back_populates='_plans')  