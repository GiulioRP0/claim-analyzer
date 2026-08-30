import pytest
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