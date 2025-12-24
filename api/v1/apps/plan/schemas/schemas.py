from pydantic import BaseModel, Field
from datetime import datetime
from  typing import Optional


class PlanSchema(BaseModel):
    client_id: str
    product_id: str
    contribution: float
    date_of_contract: datetime
    age_of_retirement: int


class PlanUpdateSchema(BaseModel):
    client_id: Optional[str] = Field(None)
    product_id: Optional[str] = Field(None)
    contribution: Optional[float] = Field(None)
    date_of_contract: Optional[datetime] = None
    age_of_retirement: Optional[int] = None

    class Config:
        orm_mode = True