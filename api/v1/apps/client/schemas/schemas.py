from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class GenderTypeEnum(str, Enum):
    Mascunlino = "Masculino"
    Feminino = "Feminino"
    Outro = "Outro"


class ClientSchema(BaseModel):
    cpf: str
    name: str
    email: str
    date_of_birth: date 
    gender: GenderTypeEnum
    monthly_income: float


class ClientUpdateSchema(BaseModel):
    cpf: Optional[str] = Field(None, max_length=11)
    name: Optional[str] = Field(None, max_length=320)
    email: Optional[str] = Field(None, max_length=320)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    monthly_income: Optional[float] = None

    class Config:
        orm_mode = True