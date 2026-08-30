from fastapi import FastAPI

from models import Claim, ClaimResponse
from analyzer import analyze_claim


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Claim Analyzer API läuft"}


@app.post("/claims", response_model=ClaimResponse)
def create_claim(claim: Claim):
    analysis = analyze_claim(claim)

    return {
        "status": "success",
        "message": "Schadenmeldung wurde analysiert.",
        "claim": claim,
        "analysis": analysis
    }