from sqlalchemy import Column, String, UUID, DECIMAL, Date, Enum
from sqlalchemy.orm import relationship
from database.session import Base
import uuid


class Client(Base):
    __tablename__ = 'client'

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    cpf = Column(String(11), nullable=False)
    name = Column(String(320), nullable=False)
    email = Column(String(320), nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum('Masculino', 'Feminino','Outro', name='gender_enum'), nullable=False)
    monthly_income = Column(DECIMAL(10, 2), nullable=False)

    _plans = relationship('Plan', back_populates='_clients')
    _extra_contributions = relationship('ExtraContribution', back_populates='_clients')
