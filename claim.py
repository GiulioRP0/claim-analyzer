from pydantic import BaseModel, Field

class Claim(BaseModel):
    contract_number: str = Field(min_length=3)
    description: str = Field(min_length=10)
    police_reported: bool