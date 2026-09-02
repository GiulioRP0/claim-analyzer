from typing import Literal

from pydantic import BaseModel, Field


class Claim(BaseModel):
    contract_number: str = Field(min_length=3)
    description: str = Field(min_length=10)
    police_reported: bool


class ClaimAnalysis(BaseModel):
    contract_number: str
    police_status: str
    description_length: int
    category: Literal["Diebstahl", "Sachschaden", "Unbekannt"]


class ClaimResponse(BaseModel):
    status: str
    message: str
    claim: Claim
    analysis: ClaimAnalysis

class CoverageAssessment(BaseModel):
    coverage_status: Literal[
        "potenziell_gedeckt",
        "nicht_gedeckt",
        "unklar",
    ]

    reason: str

    missing_information: list[str]