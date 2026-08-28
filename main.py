from claim import Claim
from input_helper import (
    ask_contract_number,
    ask_description,
    ask_police_reported,
)

print("=== Insurance Claim Analyzer ===")

contract_number = ask_contract_number()
description = ask_description()
police_reported = ask_police_reported()

claim = Claim(
    contract_number,
    description,
    police_reported
)

print()
print("--- Schadenmeldung ---")
print()
print(f"Vertragsnummer: {claim.contract_number}")
print(f"Beschreibung: {claim.description}")

if claim.police_reported:
    print("Polizei informiert: Ja")
else:
    print("Polizei informiert: Nein")