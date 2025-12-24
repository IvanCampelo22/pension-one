from sqlalchemy import Column, Integer, String, DateTime, UUID, DECIMAL
from sqlalchemy.orm import relationship
from database.session import Base
import uuid


class Products(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    name = Column(String(320), nullable=False)
    susep = Column(String(20), nullable=False)
    expiration_of_sale = Column(DateTime(320), nullable=False)
    value_minimum_aporte_initial = Column(DECIMAL(10, 2), nullable=False)
    value_minimum_aporte_extra = Column(DECIMAL(10, 2), nullable=False)
    entry_age = Column(Integer, nullable=False)
    age_of_exit = Column(Integer, nullable=False)
    lack_initial_of_rescue = Column(Integer, nullable=False)
    lack_entre_resgates = Column(Integer, nullable=False)

    _plans = relationship('Plan', back_populates='_products')
