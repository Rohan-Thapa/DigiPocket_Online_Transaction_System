from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class TransactionCreate(BaseModel):
    recipient_type: Literal['user','merchant']
    recipient_id: str
    amount: float
    description: str | None = None

class TransactionInDB(BaseModel):
    id: str | None = Field(alias="_id")
    sender_id: str
    recipient_type: Literal['user','merchant']
    recipient_id: str
    amount: float
    description: str | None = None
    status: str
    timestamp: datetime

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class TransactionOut(TransactionInDB):
    pass
