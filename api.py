from fastapi import FastAPI, HTTPException

from models import Claim, ClaimResponse
from analyzer import analyze_claim, LLMServiceError


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Claim Analyzer API läuft"}


@app.post("/claims", response_model=ClaimResponse)
def create_claim(claim: Claim):
    try:
        analysis = analyze_claim(claim)

        return {
            "status": "success",
            "message": "Schadenmeldung wurde analysiert.",
            "claim": claim,
            "analysis": analysis
        }

    except LLMServiceError:
        raise HTTPException(
            status_code=503,
            detail="Die KI-Klassifizierung ist momentan nicht verfügbar."
        )