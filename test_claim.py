import pytest
from unittest.mock import patch

from analyzer import analyze_claim
from llm_classifier import ClaimClassification
from pydantic import ValidationError

from models import Claim

def test_valid_claim():
    claim = Claim(
        contract_number="V-12345",
        description="Mein Fahrrad wurde gestohlen.",
        police_reported=True
    )

    assert claim.contract_number == "V-12345"
    assert claim.description == "Mein Fahrrad wurde gestohlen."
    assert claim.police_reported is True


def test_contract_number_too_short():
    with pytest.raises(ValidationError):
        Claim(
            contract_number="12",
            description="Mein Fahrrad wurde gestohlen.",
            police_reported=True
        )


def test_description_too_short():
    with pytest.raises(ValidationError):
        Claim(
            contract_number="V-12345",
            description="zu kurz",
            police_reported=True
        )

def test_invalid_police_reported():
    with pytest.raises(ValidationError):
        Claim(
            contract_number="V-12345",
            description="Mein Fahrrad wurde gestohlen.",
            police_reported="Banane"
        )

def test_analyze_claim_with_mocked_llm():
    claim = Claim(
        contract_number="V-12345",
        description="Jemand hat mein Fahrrad mitgenommen.",
        police_reported=True
    )

    fake_classification = ClaimClassification(
        category="Diebstahl"
    )


    with patch( #Während dieses Tests soll analyzer.py nicht die echte classify_claim()-Funktion verwenden. Gib stattdessen sofort unsere erfundene Antwort zurück.“
        "analyzer.classify_claim",
        return_value=fake_classification
    ):
        analysis = analyze_claim(claim)

    assert analysis.category == "Diebstahl"
    assert analysis.police_status == "Polizei wurde informiert."        