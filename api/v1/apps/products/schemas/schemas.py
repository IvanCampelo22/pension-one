from pydantic import BaseModel, Field 
from datetime import datetime
from typing import Optional


class ProductsSchema(BaseModel):
    name: str
    susep: str
    expiration_of_sale: datetime
    value_minimum_aporte_initial: float = 1000.00
    value_minimum_aporte_extra: float = 100.00
    entry_age: int = 18
    age_of_exit: int = 60
    lack_initial_of_rescue: int = 60
    lack_entre_resgates: int = 30


class ProductsUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=320)
    susep: Optional[str] = Field(None, max_length=20)
    expiration_of_sale: Optional[datetime] = None
    value_minimum_aporte_initial: Optional[float] = None
    value_minimum_aporte_extra: Optional[float] = None
    entry_age: Optional[int] = None
    age_of_exit: Optional[int] = None
    lack_initial_of_rescue: Optional[int] = None
    lack_entre_resgates: Optional[int] = None

    class Config:
        orm_mode = True