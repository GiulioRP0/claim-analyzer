from models import Claim, ClaimAnalysis
from llm_classifier import classify_claim


def analyze_claim(claim: Claim) -> ClaimAnalysis:
    classification = classify_claim(claim.description)

    if claim.police_reported:
        police_status = "Polizei wurde informiert."
    else:
        police_status = "Polizei wurde nicht informiert."

    return ClaimAnalysis(
        contract_number=claim.contract_number,
        police_status=police_status,
        description_length=len(claim.description),
        category=classification.category
    )