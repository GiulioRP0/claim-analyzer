from models import Claim, ClaimAnalysis


def analyze_claim(claim: Claim) -> ClaimAnalysis:
    description = claim.description.lower()

    if "gestohlen" in description or "diebstahl" in description:
        category = "Diebstahl"

    elif "beschädigt" in description or "kaputt" in description:
        category = "Sachschaden"

    else:
        category = "Unbekannt"

    if claim.police_reported:
        police_status = "Polizei wurde informiert."
    else:
        police_status = "Polizei wurde nicht informiert."

    return ClaimAnalysis(
        contract_number=claim.contract_number,
        police_status=police_status,
        description_length=len(claim.description),
        category=category
    )