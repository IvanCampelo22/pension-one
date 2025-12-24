from pydantic import BaseModel, Field
from typing import Optional


class ExtraContributionSchema(BaseModel):
    client_id: str
    plan_id: str
    contribution_value: float
    

class ExtraContributionUpdateSchema(BaseModel):
    client_id: Optional[str] = Field(None)
    plan_id: Optional[str] = Field(None)
    contribution_value: Optional[float] = Field(None)