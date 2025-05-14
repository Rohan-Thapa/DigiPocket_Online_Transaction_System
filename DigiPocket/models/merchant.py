from pydantic import BaseModel, Field

class MerchantCreate(BaseModel):
    name: str
    description: str | None = None

class MerchantInDB(BaseModel):
    id: str | None = Field(alias="_id")
    name: str
    description: str | None = None
    balance: float = 0.0

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class MerchantOut(BaseModel):
    id: str
    name: str
    description: str | None = None
    balance: float