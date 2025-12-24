from pydantic import BaseModel, Field
from typing import Optional


class RescueSchema(BaseModel):
    plan_id: str
    rescue_value: float
    

class RescueUpdateSchema(BaseModel):
    plan_id: Optional[str] = Field(None)
    rescue_value: Optional[float] = Field(None)

    class Config:
        orm_mode = True
    