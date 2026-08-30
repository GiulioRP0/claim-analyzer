from pydantic import BaseModel, Field


class Claim(BaseModel):
    contract_number: str = Field(min_length=3)
    description: str = Field(min_length=10)
    police_reported: bool


class ClaimAnalysis(BaseModel):
    contract_number: str
    police_status: str
    description_length: int
    category: str


class ClaimResponse(BaseModel):
    status: str
    message: str
    claim: Claim
    analysis: ClaimAnalysis